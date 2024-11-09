from models import User, Product, Order, OrderItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from engine import DATABASE_URL

engine = create_engine(DATABASE_URL)

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()

# Query all users
users = session.query(User).all()
for user in users:
    print(f"User: {user.username}, Email: {user.email}")

# Query a user's orders
user_orders = session.query(Order).filter_by(user_id=1).all()
for order in user_orders:
    print(f"Order ID: {order.order_id}, Created At: {order.created_at}")
