class Product:
    def __init__(self, name, price, description=''):
        self.name = name
        self.price = price
        self.description = description

    def __str__(self):
        return f'{self.name} - {self.price}'


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

    def add_product(self, product):
        self.items.append(product)

    def remove_product(self, product):
        self.items.remove(product)

    def get_total_price(self):
        return sum(item.price for item in self.items)

    def __str__(self):
        cart_contents = ', '.join([str(item) for item in self.items])
        return f'Cart: {cart_contents} | Total: {self.get_total_price()}'

class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = customer.cart.items.copy()
        self.total = customer.cart.get_total_price()

    def __str__(self):
        items = ', ',join([str(item) for item in self.items])
        return f'Order for {self.customer.name}: {items} | Total: {self.total}'


# Создаем несколько товаров
product1 = Product("Laptop", 999.99, "A powerful laptop")
product2 = Product("Mouse", 49.99, "Wireless mouse")

# Создаем клиента
customer = Customer("Alice", "alice@example.com")

# Клиент добавляет товары в корзину
customer.cart.add_product(product1)
customer.cart.add_product(product2)

# Выводим информацию о корзине клиента
print(customer.cart)

# Клиент оформляет заказ
order = Order(customer)
print(order)
