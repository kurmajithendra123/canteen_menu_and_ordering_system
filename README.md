# College Canteen Ordering System

A web-based ordering system to reduce queues in college canteens.

## Features
*   **Digital Menu**: Browse items with images and prices.
*   **Cart & Checkout**: Add items, adjust quantity, and "pay" (mock).
*   **QR Code Verification**: Generates a unique QR code for every order.
*   **Admin Dashboard**: Manage order status (Received -> Completed).

## Setup & Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Initialize Database**:
    ```bash
    python seed.py
    ```
    (This creates `canteen.db` and adds sample menu items).

3.  **Run the App**:
    ```bash
    python app.py
    ```
    Access the app at `http://127.0.0.1:5000`.

## Usage Flow
1.  **Student**: Opens homepage (`/`), adds items to cart, clicks "Pay & Place Order".
2.  **Confirmation**: Sees "Order Placed Successfully" screen with a **QR Code**.
3.  **Pickup**: Shows QR code at the counter.
4.  **Admin/Staff**: Opens `/admin` to see the order. Changing status to "Ready" or "Completed" updates the system.

## Project Structure
*   `app.py`: Main Flask application and API.
*   `models.py`: Database schema.
*   `static/`: CSS, JS, and generated QR codes.
*   `templates/`: HTML files.
