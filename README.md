# Pizza Ordering System APIs and ViewSets

This README provides an overview of the APIs and ViewSets available in the Pizza Ordering System Django application. This application allows users to place and manage pizza orders, including customizing pizzas with various toppings and tracking the status of their orders.

## Table of Contents

1. [Installation](#installation)
2. [API Endpoints](#api-endpoints)
    - [Orders](#orders)
    - [Pizzas](#pizzas)
3. [ViewSets](#viewsets)
    - [OrdersViewSet](#ordersviewset)
    - [PizzaViewSet](#pizzaviewset)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

## Installation

1. Clone the project repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Migrate the database using `python manage.py migrate`.
4. Create a superuser using `python manage.py createsuperuser`.
5. Start the development server using `python manage.py runserver`.

## API Endpoints

### Orders

- `POST /api/orders/place_order/?id=<order_id>`: Place an order with a specified order ID.
- `GET /api/orders/`: List all orders.
- `GET /api/orders/<order_id>/`: Retrieve details of a specific order.

### Pizzas

- `POST /api/pizzas/add_pizza_to_cart/`: Add a pizza to the cart.
- `POST /api/pizzas/remove_pizza_from_cart/?id=<pizza_id>`: Remove a pizza from the cart.

## ViewSets

### OrdersViewSet

- `place_order`: Place an order with the specified order ID.

### PizzaViewSet

- `add_pizza_to_cart`: Add a pizza to the cart.
- `remove_pizza_from_cart`: Remove a pizza from the cart.

## Usage

- Access the Django admin interface at `http://localhost:8000/admin/` to manage orders, toppings, and other data.
- Use the API endpoints to interact with the application programmatically.

  # Pizza Zen Application

This is the README for the Pizza Zen application, which allows you to order delicious pizzas.

## Running with Docker

To run the Pizza Zen application using Docker, follow these steps:

1. Make sure you have Docker installed on your system. If not, you can download and install it from [Docker's official website](https://www.docker.com/get-started).

2. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/pizza-zen.git
   cd pizza-zen
   docker-compose build
   docker-compose exec backend bash
   python manage.py createsuperuser
   docker-compose up
   
