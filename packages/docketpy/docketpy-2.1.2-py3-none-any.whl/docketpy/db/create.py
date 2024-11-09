from models import User, Product, Order, OrderItem, Workspace
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from engine import DATABASE_URL

engine = create_engine(DATABASE_URL)

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()

# Create a new user
new_user = User(username="john_doe", email="john@example.com", password="securepassword")
session.add(new_user)
session.commit()

# Create a new product
new_product = Product(name="Laptop", description="A powerful laptop", price=1200.00)
session.add(new_product)
session.commit()

# Create an order for the user
order = Order(user=new_user)
session.add(order)
session.commit()

# Add an order item linking the product and order
order_item = OrderItem(order=order, product=new_product, quantity=1)
session.add(order_item)
session.commit()

new_ws = Workspace(name="test_workspace", location="test_location", logs_bucket="test_logs_bucket", url="test_url")
session.add(new_ws)
session.commit()