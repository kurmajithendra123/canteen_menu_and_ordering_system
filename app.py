import os
import json
import uuid
from flask import Flask, render_template, jsonify, request, url_for, redirect, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, MenuItem, Order, OrderItem, User
import qrcode
from datetime import datetime

def create_app():
    app = Flask(__name__)
    # Use DATABASE_URL from environment (for Render/Postgres) or fallback to local SQLite
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///canteen.db')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    
    os.makedirs(os.path.join(app.root_path, 'static', 'qrcodes'), exist_ok=True)

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        # Landing Page: Canteen Selection
        return render_template('select_canteen.html')

    @app.route('/canteen/<canteen_name>')
    def menu_page(canteen_name):
        return render_template('index.html', canteen_name=canteen_name)

    # --- Auth Routes ---
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('index'))
            flash('Invalid username or password')
        return render_template('login.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            captcha_input = request.form.get('captcha')
            
            # 1. Validate Password Match
            if password != confirm_password:
                flash('Passwords do not match')
                return redirect(url_for('signup'))

            # 2. Validate Captcha
            if 'captcha_result' not in session or not captcha_input:
                 flash('Captcha Error. Please try again.')
                 return redirect(url_for('signup'))
            
            try:
                if int(captcha_input) != session['captcha_result']:
                    flash('Incorrect Captcha')
                    return redirect(url_for('signup'))
            except ValueError:
                flash('Invalid Captcha')
                return redirect(url_for('signup'))

            # 3. Check Username
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
                return redirect(url_for('signup'))
            
            # 4. Create User
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)
            return redirect(url_for('index'))
            
        # GET Request: Generate Captcha
        import random
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        session['captcha_result'] = num1 + num2
        captcha_question = f"{num1} + {num2}"
        
        return render_template('signup.html', captcha_question=captcha_question)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    # --- API Routes ---
    @app.route('/api/menu')
    def get_menu():
        canteen_filter = request.args.get('canteen')
        if canteen_filter:
            items = MenuItem.query.filter_by(available=True, canteen=canteen_filter).all()
        else:
            items = MenuItem.query.filter_by(available=True).all()
            
        return jsonify([item.to_dict() for item in items])

    @app.route('/api/order', methods=['POST'])
    def place_order():
        try:
            data = request.json
            items = data.get('items', [])
            
            if not items:
                return jsonify({'success': False, 'error': 'No items in order'}), 400

            # Determine User
            user_id = current_user.id if current_user.is_authenticated else None
            customer_name = current_user.username if current_user.is_authenticated else data.get('customer_name', 'Guest')

            total_amount = 0
            order_items = []
            order_id = str(uuid.uuid4())
            
            for item_data in items:
                item_id = int(item_data['id'])
                menu_item = MenuItem.query.get(item_id)
                if menu_item:
                    qty = int(item_data['quantity'])
                    price = menu_item.price
                    total_amount += price * qty
                    
                    order_item = OrderItem(
                        order_id=order_id,
                        item_menu_id=menu_item.id,
                        item_name=menu_item.name,
                        quantity=qty,
                        price_at_time=price
                    )
                    order_items.append(order_item)

            new_order = Order(
                id=order_id,
                user_id=user_id,
                customer_name=customer_name,
                total_amount=total_amount,
                status='Received'
            )
            
            # QR Gen
            qr_data = json.dumps({
                "id": order_id,
                "name": customer_name,
                "total": total_amount,
                "ts": datetime.now().isoformat()
            })
            
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Create Receipt Image w/ Theme
            from PIL import Image, ImageDraw, ImageFont
            
            # Theme Colors
            PRIMARY_COLOR = "#be123c"
            TEXT_MAIN = "#1f2937"
            TEXT_MUTED = "#6b7280"
            BG_COLOR = "#ffffff"

            # High Res Canvas
            receipt_width = 800
            # Estimate height dynamically
            header_height = 140
            item_height = 50
            footer_height = 400
            receipt_height = header_height + 250 + (len(order_items) * item_height) + footer_height
            
            receipt = Image.new('RGB', (receipt_width, receipt_height), BG_COLOR)
            draw = ImageDraw.Draw(receipt)
            
            # Fonts (Try standard Windows fonts for better look)
            try:
                title_font = ImageFont.truetype("arialbd.ttf", 50)
                heading_font = ImageFont.truetype("arialbd.ttf", 32)
                body_font = ImageFont.truetype("arial.ttf", 28)
                small_font = ImageFont.truetype("arial.ttf", 24)
            except:
                # Fallback
                title_font = ImageFont.load_default()
                heading_font = ImageFont.load_default()
                body_font = ImageFont.load_default()
                small_font = ImageFont.load_default()

            # --- Header ---
            try:
                # Try loading a standard font, fallback to default if fails
                font_large = ImageFont.truetype("arial.ttf", 24)
                font_med = ImageFont.truetype("arial.ttf", 18)
                font_small = ImageFont.truetype("arial.ttf", 14)
            except:
                font_large = ImageFont.load_default()
                font_med = ImageFont.load_default()
                font_small = ImageFont.load_default()

            # --- Header ---
            draw.rectangle([(0, 0), (receipt_width, header_height)], fill=PRIMARY_COLOR)
            draw.text((receipt_width//2, header_height//2), "CAMPUS CANTEEN", font=title_font, fill="white", anchor="mm")
            
            y = header_height + 40
            
            # --- Order Info (Left) ---
            draw.text((40, y), f"Order Receipt", font=heading_font, fill=TEXT_MAIN)
            y += 50
            draw.text((40, y), f"Order #: {order_id[:8]}", font=body_font, fill=TEXT_MAIN)
            y += 40
            draw.text((40, y), f"Customer: {customer_name}", font=body_font, fill=TEXT_MAIN)
            y += 40
            draw.text((40, y), f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", font=body_font, fill=TEXT_MUTED)
            y += 60
            
            # --- Items Table ---
            # Header
            draw.rectangle([(40, y), (receipt_width-40, y+50)], fill="#f3f4f6")
            draw.text((60, y+10), "Item", font=body_font, fill=TEXT_MAIN)
            draw.text((receipt_width-60, y+10), "Price", font=body_font, fill=TEXT_MAIN, anchor="ra")
            y += 60
            
            # List
            for item in order_items:
                name_short = (item.item_name[:35] + '..') if len(item.item_name) > 35 else item.item_name
                line = f"{item.quantity}x  {name_short}"
                price_str = f"Rs {item.price_at_time * item.quantity}"
                
                draw.text((60, y), line, font=body_font, fill=TEXT_MAIN)
                draw.text((receipt_width-60, y), price_str, font=body_font, fill=TEXT_MAIN, anchor="ra")
                y += item_height
                
            # --- Total ---
            y += 20
            draw.line((40, y, receipt_width-40, y), fill=PRIMARY_COLOR, width=3)
            y += 30
            draw.text((40, y), "TOTAL AMOUNT:", font=heading_font, fill=TEXT_MAIN)
            draw.text((receipt_width-40, y), f"Rs {total_amount}", font=title_font, fill=PRIMARY_COLOR, anchor="ra")
            y += 80
            
            # --- QR Code ---
            # 1. Save Raw QR (For Display on Website)
            qr_filename = f"{order_id}.png"
            qr_path = os.path.join('static', 'qrcodes', qr_filename)
            full_qr_path = os.path.join(app.root_path, qr_path)
            qr_img.save(full_qr_path)

            # 2. Resize and Paste for Receipt (For Download)
            target_qr_size = 350
            # Resize copy for receipt - create new instance
            qr_resized = qr_img.resize((target_qr_size, target_qr_size), resample=Image.Resampling.LANCZOS)
            
            qr_x = (receipt_width - target_qr_size) // 2
            receipt.paste(qr_resized, (qr_x, y))
            
            # Footer text
            y += target_qr_size + 20
            draw.text((receipt_width//2, y), "Scan to verify order", font=small_font, fill=TEXT_MUTED, anchor="mm")
            
            # Save Receipt to SEPARATE file
            receipt_filename = f"{order_id}_receipt.png"
            receipt_path = os.path.join('static', 'qrcodes', receipt_filename)
            full_receipt_path = os.path.join(app.root_path, receipt_path)
            receipt.save(full_receipt_path, quality=95)
            
            # DB points to RAW QR (so website displays it)
            new_order.qr_code_path = f"static/qrcodes/{qr_filename}"

            db.session.add(new_order)
            for oi in order_items:
                db.session.add(oi)
            db.session.commit()
            
            return jsonify({'success': True, 'order_id': order_id})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/order/<order_id>')
    def order_status(order_id):
        order = Order.query.get_or_404(order_id)
        return render_template('order.html', order=order)

    # --- Admin Routes ---
    
    @app.route('/admin')
    @login_required
    def admin_dashboard():
        if not current_user.is_admin:
            flash("Access Denied")
            return redirect(url_for('index'))
            
        orders = Order.query.order_by(Order.timestamp.desc()).all()
        return render_template('admin.html', orders=orders)

    @app.route('/admin/menu')
    @login_required
    def admin_menu():
        if not current_user.is_admin:
            flash("Access Denied")
            return redirect(url_for('index'))
            
        canteen_filter = request.args.get('canteen')
        canteens = ["Main Canteen Ab1", "MBA canteen", "IT canteen AB3"]
        
        if canteen_filter:
            items = MenuItem.query.filter_by(canteen=canteen_filter).all()
        else:
            items = MenuItem.query.all()
        
        # Serialize for JS
        items_data = [item.to_dict() for item in items]
            
        return render_template('admin_menu.html', items=items, items_data=items_data, canteens=canteens, current_canteen=canteen_filter)

    @app.route('/admin/menu/add', methods=['POST'])
    @login_required
    def add_menu_item():
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 401
            
        try:
            name = request.form.get('name')
            price = float(request.form.get('price'))
            category = request.form.get('category')
            canteen = request.form.get('canteen')
            image_url = request.form.get('image_url')
            # Handle quantity, defaulting to 0 if not provided
            quantity = int(request.form.get('quantity', 0))
            available = request.form.get('available') == 'on'
            
            new_item = MenuItem(
                name=name, price=price, category=category,
                canteen=canteen, image_url=image_url, 
                quantity=quantity, available=available
            )
            db.session.add(new_item)
            db.session.commit()
            flash(f"Added {name} successfully")
        except Exception as e:
            flash(f"Error adding item: {str(e)}")
            
        return redirect(url_for('admin_menu'))

    @app.route('/admin/menu/edit/<int:item_id>', methods=['POST'])
    @login_required
    def edit_menu_item(item_id):
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 401
            
        item = MenuItem.query.get_or_404(item_id)
        
        item.name = request.form.get('name')
        item.price = float(request.form.get('price'))
        item.quantity = int(request.form.get('quantity', 0))
        item.category = request.form.get('category')
        item.canteen = request.form.get('canteen')
        item.image_url = request.form.get('image_url')
        item.available = request.form.get('available') == 'on'
        
        db.session.commit()
        flash(f"Updated {item.name}")
        return redirect(url_for('admin_menu'))

    @app.route('/admin/menu/delete/<int:item_id>', methods=['POST'])
    @login_required
    def delete_menu_item(item_id):
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 401
            
        item = MenuItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True})

    @app.route('/api/admin/order/<order_id>/status', methods=['POST'])
    def update_status(order_id):
        data = request.json
        status = data.get('status')
        order = Order.query.get(order_id)
        if order:
            order.status = status
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Order not found'}), 404

    @app.route('/api/orders/batch', methods=['POST'])
    def get_batch_orders():
        data = request.json
        order_ids = data.get('order_ids', [])
        
        if current_user.is_authenticated:
            # Fetch orders belonging to user OR orders from the local storage list THAT ARE GUEST ORDERS
            # Do NOT show orders from local storage if they belong to another user
            if order_ids:
                orders = Order.query.filter(
                    (Order.user_id == current_user.id) | 
                    ((Order.id.in_(order_ids)) & (Order.user_id.is_(None)))
                ).order_by(Order.timestamp.desc()).all()
            else:
                orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.timestamp.desc()).all()
        else:
            if not order_ids:
                return jsonify([])
            # Guests can ONLY see orders that do not belong to any user (user_id is None)
            orders = Order.query.filter(
                Order.id.in_(order_ids) & Order.user_id.is_(None)
            ).order_by(Order.timestamp.desc()).all()
            
        return jsonify([order.to_dict() for order in orders])

    @app.route('/my-orders')
    @login_required
    def my_orders():
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.timestamp.desc()).all()
        return render_template('my_orders.html', orders=orders)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
