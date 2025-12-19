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
*   **Admin**: admin and password is admin123
* admin can manage the food items according to the quantity(updated the quatity part).
*   **Students**: Sign up nicely!

## Deployed url: https://canteen-menu-and-ordering-system.onrender.com
* Deployed it on render

## css and style:
*  Css and Style of the website taken from the myamrita portal because it is very easy while integrating with myamrita website.(This is the real problem that had been there in the collage.)


## Another idea to be developed:
* We can develop this according to the time slot, in each time slot some students can go, like wise if we do that, there are some other problem will be occured.
* CASE 1: if mess food was not nice then definetly the student will go the canteen(at the same time canteen has no available slots to book). What is the purpose of keeping time slots.
* CASE 2: suppose student have a project review at 1pm and it took one hour to complete. By 2pm mess will be closed then definetly every student will choose to go canteen. if slots are full and items are available (canteen is occupied but items are available).
* CASE 3: some may work for projects in the canteen spending hours of time because of system shows slots are full and food will be wasted.
* There are many scenarios like wise which tells that time slots will not work in collage canteens.

* BY seeing this many cons i haven't included time slots. (Time slots will only work for the restaurents not for the collage canteens).


## Total purpose of this project is to reduce the time spent in the queues to collect the food.
