import sqlite3

def add_quantity_column():
    conn = sqlite3.connect('instance/canteen.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE menu_item ADD COLUMN quantity INTEGER DEFAULT 0")
        conn.commit()
        print("Successfully added 'quantity' column to menu_item table.")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e):
            print("'quantity' column already exists.")
        else:
            print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_quantity_column()
