from models import User, Product, Order, OrderItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from engine import DATABASE_URL

engine = create_engine(DATABASE_URL)

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()

# Delete an order
order_to_delete = session.query(Order).filter_by(order_id=1).first()
session.delete(order_to_delete)
session.commit()
