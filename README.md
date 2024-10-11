# E-commerce
An E-commerce system focused on cart management, inventory handling, and cart reporting for large datasets.

## Key Features

### Cart & Cart Item Management
- Add items to the cart seamlessly.
- Cart expiration: Automatically expire carts after a set period of time.
- Graceful handling of expired carts and inventory restoration.

### Product & Inventory Management
- Robust product catalog system with real-time stock and inventory tracking.
- Automatic stock updates based on cart activity and order completion.

### Optimized Daily Reports
- Generate cart reports by day showing each user’s total cart value.
- Efficiently handle large datasets with optimized queries for fast reporting.
- Pagination support to ensure scalable reporting for high-volume data.

## Technologies
- **Django**: Backend framework for handling business logic and cart expiration.
- **Django REST Framework**: API for cart and product management.
- **Celery** : Task queue for background cart expiration checks.
- **Redis**: broker for task queuing.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/MahsaRah99/ecommerce-platform.git
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Run the development server:
    ```bash
    python manage.py runserver
    ```

