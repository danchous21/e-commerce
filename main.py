class Product:
    def __init__(self, name, price, description="", category=None, stock=0):
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.stock = stock

        if category:
            category.add_product(self)

    def is_in_stock(self):
        return self.stock > 0

    def reduce_stock(self, quantity):
        if quantity <= self.stock:
            self.stock -= quantity
            return True
        return False

    def __str__(self):
        stock_status = f"In Stock: {self.stock}" if self.stock > 0 else "Out of Stock"
        return f"{self.name} - ${self.price} ({self.category.name if self.category else 'No Category'}) | {stock_status}"


class Category:
    def __init__(self, name):
        self.name = name
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        product.category = self

    def __str__(self):
        return f'Category: {self.name}'


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
        # Теперь учитываем, что self.items содержит кортежи (product, quantity)
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


# Создаем несколько категорий
electronics = Category("Electronics")
clothing = Category("Clothing")

# Создаем несколько товаров с учетом категорий и наличия на складе
laptop = Product("Laptop", 999.99, "A powerful laptop", electronics, stock=5)
mouse = Product("Mouse", 49.99, "Wireless mouse", electronics, stock=10)
shirt = Product("Shirt", 19.99, "Cotton T-shirt", clothing, stock=3)

# Создаем клиента
customer = Customer("Alice", "alice@example.com")

# Клиент добавляет товары в корзину
customer.cart.add_product(laptop, quantity=2)
customer.cart.add_product(mouse, quantity=1)
customer.cart.add_product(shirt, quantity=5)  # Пробуем добавить больше, чем в наличии

# Выводим информацию о корзине клиента
print(customer.cart)

# Создаем скидку и применяем ее к заказу
discount = Discount("Summer Sale", 10)  # 10% скидка
order = Order(customer, discount)
print(order)

