# CampusCanteen - College Canteen Ordering System 🍔

A full-stack web application designed to reduce queues and streamline food ordering in college canteens.

The absence of a digital menu and ordering system in college canteens leads to long queues, time wastage, and inefficient order management. This project solves that by allowing students to order from their phones and pick up when ready.

## Features ✨

### For Students 🎓
*   **Digital Menu**: Browse authentic items with images, prices, and stock status.
*   **Stock Tracking**: See real-time availability ("Only X left" or "Out of Stock").
*   **Cart & Checkout**: Add items, adjust quantities, and place orders directly.
*   **QR Code Receipts**: Receive a unique QR code for every successful order.

### For Admin/Staff 👨‍🍳
*   **Admin Dashboard**: Manage incoming orders and update status (Received -> Ready -> Completed).
*   **Menu Management**: Add, Edit, and Delete menu items.
*   **Inventory Control**: Set quantity/stock levels for each item.
*   **Multi-Canteen Support**: Manage menus for different canteens (Main, MBA, IT Block).

## Setup & Run 🚀

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Initialize Database**:
    ```bash
    python seed.py
    ```
    *(Creates `instance/canteen.db` and populates it with sample data).*

3.  **Run the App**:
    ```bash
    python app.py
    ```
    Access the app at `http://127.0.0.1:5000`.

## Project Structure 📂
*   `app.py`: Main Flask application (Routes & Logic).
*   `models.py`: Database schema (User, Menu, Order).
*   `templates/`: HTML files (Jinja2).
*   `static/`: CSS styling, JavaScript logic, and generated QR codes.

## Login Details 🔑
*   **Admin**: `admin` / `admin123`
*   **Students**: Sign up nicely!
