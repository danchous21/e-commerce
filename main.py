import logging

from models import Product, Category, Customer, Discount

from database import Database
from logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


def main():
    try:

        db = Database()
        db.create_tables()

        electronics = Category("Electronics")
        electronics.save(db)
        logger.info("Category 'Electronics' created and saved.")

        laptop = Product("Laptop", 999.99, "A powerful laptop", electronics, stock=5)
        laptop.save(db)
        logger.info(f"Product 'Laptop' created and saved with ID {laptop.id}.")

        retrieved_laptop = Product.get_by_id(db, laptop.id)
        if retrieved_laptop:
            logger.info(f"Product retrieved: {retrieved_laptop}")
        else:
            logger.warning("Product not found.")

        db.close()

        customer = Customer("Alice", "alice@example.com")

        customer.cart.add_product(laptop, quantity=2)
        customer.cart.add_product(mouse, quantity=1)
        customer.cart.add_product(shirt, quantity=5)

        logger.info(f"Shopping Cart: {customer.cart}")

        discount = Discount("Summer Sale", 10)
        logger.info(f"Order created: {order}")

    except Exception as e:
        logger.error("An error occurred", exc_info=True)


if __name__ == "__main__":
    main()
