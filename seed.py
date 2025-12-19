from app import app, db
from models import MenuItem

def seed_database():
    with app.app_context():
        # Check if items exist
        if MenuItem.query.first():
            print("Database already seeded.")
            return

        items = [
            MenuItem(name="Veg Burger", price=50.0, category="Snacks", image_url="https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=500&auto=format&fit=crop&q=60"),
            MenuItem(name="Chicken Sandwich", price=80.0, category="Snacks", image_url="https://images.unsplash.com/photo-1521305916504-4a1121188589?w=500&auto=format&fit=crop&q=60"),
            MenuItem(name="Masala Dosa", price=60.0, category="Breakfast", image_url="https://images.unsplash.com/photo-1668236540372-969c36209d84?w=500&auto=format&fit=crop&q=60"),
            MenuItem(name="Idli Vada", price=40.0, category="Breakfast", image_url="https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=500&auto=format&fit=crop&q=60"),
            MenuItem(name="Cold Coffee", price=40.0, category="Beverages", image_url="https://images.unsplash.com/photo-1578314675249-a6910f80cc4e?w=500&auto=format&fit=crop&q=60"),
            MenuItem(name="Tea", price=15.0, category="Beverages", image_url="https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500&auto=format&fit=crop&q=60"),
            MenuItem(name="Hakka Noodles", price=90.0, category="Lunch", image_url="https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500&auto=format&fit=crop&q=60"),
            MenuItem(name="Fried Rice", price=80.0, category="Lunch", image_url="https://images.unsplash.com/photo-1603133872878-684f57143b34?w=500&auto=format&fit=crop&q=60"),
        ]

        db.session.bulk_save_objects(items)
        db.session.commit()
        print("Database seeded successfully with sample items!")

if __name__ == "__main__":
    seed_database()
