from app import app, db
from models import MenuItem

def reset_database():
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()

        print("Seeding menu items...")
        
        # Canteen NAMES
        canteens = ["Main Canteen Ab1", "MBA canteen", "IT canteen AB3"]
        
        items = [
            # Main Canteen Ab1
            MenuItem(name="Veg Burger", price=50.0, category="Snacks", image_url="https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=500&auto=format&fit=crop&q=60", canteen=canteens[0]),
            MenuItem(name="Chicken Sandwich", price=80.0, category="Snacks", image_url="https://images.unsplash.com/photo-1521305916504-4a1121188589?w=500&auto=format&fit=crop&q=60", canteen=canteens[0]),
            MenuItem(name="Fried Rice", price=70.0, category="Lunch", image_url="https://images.unsplash.com/photo-1603133872878-684f57143b34?w=500&auto=format&fit=crop&q=60", canteen=canteens[0]),
            
            # MBA canteen
            MenuItem(name="Cold Coffee", price=40.0, category="Beverages", image_url="https://images.unsplash.com/photo-1578314675249-a6910f80cc4e?w=500&auto=format&fit=crop&q=60", canteen=canteens[1]),
            MenuItem(name="Samosa", price=15.0, category="Snacks", image_url="https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&auto=format&fit=crop&q=60", canteen=canteens[1]),
            MenuItem(name="Pizza Slice", price=60.0, category="Snacks", image_url="https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&auto=format&fit=crop&q=60", canteen=canteens[1]),

            # IT canteen AB3
            MenuItem(name="Masala Dosa", price=45.0, category="Breakfast", image_url="https://images.unsplash.com/photo-1668236540372-969c36209d84?w=500&auto=format&fit=crop&q=60", canteen=canteens[2]),
            MenuItem(name="Tea", price=10.0, category="Beverages", image_url="https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500&auto=format&fit=crop&q=60", canteen=canteens[2]),
            MenuItem(name="Noodles", price=55.0, category="Lunch", image_url="https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500&auto=format&fit=crop&q=60", canteen=canteens[2]),
        ]

        db.session.bulk_save_objects(items)
        
        # Create Admin User
        from models import User
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', is_admin=True)
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            
        db.session.commit()
        print("Database reset and seeded successfully!")
        print("Default Admin: admin / admin123")

if __name__ == "__main__":
    reset_database()
