import psycopg2


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

    def create_tables(self):
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

    def close(self):
        self.cur.close()
        self.conn.close()
