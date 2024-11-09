from models import User, Product, Order, OrderItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from engine import DATABASE_URL

engine = create_engine(DATABASE_URL)

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()

# Update a product's price
product_to_update = session.query(Product).filter_by(name="Laptop").first()
product_to_update.price = 1100.00
session.commit()
