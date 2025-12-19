import json
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    canteen = db.Column(db.String(100), nullable=False, default="Main Canteen Ab1")
    available = db.Column(db.Boolean, default=True)
    quantity = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image_url': self.image_url,
            'category': self.category,
            'canteen': self.canteen,
            'available': self.available,
            'quantity': self.quantity
        }

class Order(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Nullable for guest orders
    customer_name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Received')
    timestamp = db.Column(db.DateTime, default=datetime.now)
    qr_code_path = db.Column(db.String(255), nullable=True)
    
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'total_amount': self.total_amount,
            'status': self.status,
            'timestamp': self.timestamp.isoformat(),
            'qr_code_path': self.qr_code_path,
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(36), db.ForeignKey('order.id'), nullable=False)
    item_menu_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=True)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'item_name': self.item_name,
            'quantity': self.quantity,
            'price': self.price_at_time
        }
