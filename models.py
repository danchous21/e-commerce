class Product:
    def __init__(self, name, price, description="", category=None, stock=0, id=None):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.stock = stock

    def save(self, db):
        if self.id is None:
            db.cur.execute(
                """
                INSERT INTO products (name, price, description, category_id, stock)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """,
                (self.name, self.price, self.description, self.category.id if self.category else None, self.stock)
            )
            self.id = db.cur.fetchone()[0]
        else:
            db.cur.execute(
                """
                UPDATE products SET name = %s, price = %s, description = %s, category_id = %s, stock = %s
                WHERE id = %s;
                """,
                (self.name, self.price, self.description, self.category.id if self.category else None, self.stock, self.id)
            )
        db.conn.commit()

    @staticmethod
    def get_by_id(db, id):
        db.cur.execute("SELECT id, name, price, description, category_id, stock FROM products WHERE id = %s;", (id,))
        row = db.cur.fetchone()
        if row:
            category = Category.get_by_id(db, row[4])
            return Product(id=row[0], name=row[1], price=row[2], description=row[3], category=category, stock=row[5])
        return None


class Category:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
        self.products = []

    def save(self, db):
        if self.id is None:
            db.cur.execute(
                "INSERT INTO categories (name) VALUES (%s) RETURNING id;",
                (self.name,)
            )
            self.id = db.cur.fetchone()[0]
        else:
            db.cur.execute(
                "UPDATE categories SET name = %s WHERE id = %s;",
                (self.name, self.id)
            )
        db.conn.commit()

    @staticmethod
    def get_by_id(db, id):
        db.cur.execute("SELECT id, name FROM categories WHERE id = %s;", (id,))
        row = db.cur.fetchone()
        if row:
            return Category(id=row[0], name=row[1])
        return None


class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.cart = ShoppingCart()

    def __str__(self):
        return f'Customer: {self.name}< Email: {self.email}'


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_product(self, product, quantity=1):
        if product.is_in_stock() and product.reduce_stock(quantity):
            self.items.append((product, quantity))
        else:
            print(f"Sorry, {product.name} is out of stock.")

    def get_total_price(self):
        return sum(item[0].price * item[1] for item in self.items)

    def __str__(self):
        cart_contents = ", ".join([f"{item[0].name} (x{item[1]})" for item in self.items])
        return f"Cart: {cart_contents} | Total: ${self.get_total_price()}"



class Order:
    def __init__(self, customer, discount=None):
        self.customer = customer
        self.items = customer.cart.items.copy()
        self.discount = discount
        self.total = self.calculate_total()

    def calculate_total(self):
        total = sum(item[0].price * item[1] for item in self.items)
        if self.discount:
            total = self.discount.apply_discount(total)
        return total

    def __str__(self):
        items = ", ".join([f"{item[0].name} (x{item[1]})" for item in self.items])
        discount_info = f" | Applied: {self.discount}" if self.discount else ""
        return f"Order for {self.customer.name}: {items} | Total: ${self.total}{discount_info}"

class Discount:
    def __init__(self, description, percentage):
        self.description = description
        self.percentage = percentage

    def apply_discount(self, amount):
        discount_amount = amount * (self.percentage / 100)
        return amount - discount_amount

    def __str__(self):
        return f"Discount: {self.description} - {self.percentage}%"