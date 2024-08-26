from database import Database
from models import Category, Product

db = Database()
db.create_tables()

electronics = Category("Electronics")
electronics.save(db)

laptop = Product("Laptop", 999.99, "A powerful laptop", electronics, stock=5)
laptop.save(db)

retrieved_laptop = Product.get_by_id(db, laptop.id)
print(retrieved_laptop)

db.close()
