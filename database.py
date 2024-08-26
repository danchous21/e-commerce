import psycopg2
import logging
from logging_config import setup_logging


setup_logging()
logger = logging.getLogger(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="ecommerce",
        user="ecommerce_user",
        password="your_password",
        host="localhost",
        options="-c client_encoding=UTF8"
    )
    return conn

class Database:
    def __init__(self):
        self.conn = get_db_connection()
        self.cur = self.conn.cursor()
        logger.info("Database connection established.")

    def create_tables(self):
        try:
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
            """)
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                description TEXT,
                category_id INTEGER REFERENCES categories(id),
                stock INTEGER NOT NULL
            );
            """)
            self.conn.commit()
            logger.info("Tables created successfully.")
        except Exception as e:
            logger.error("Failed to create tables", exc_info=True)
            raise

    def close(self):
        self.cur.close()
        self.conn.close()
        logger.info("Database connection closed.")
