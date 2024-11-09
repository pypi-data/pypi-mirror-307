from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import database_exists, create_database

# Database connection URL for your database server (without specifying a database)
DATABASE_URL = "postgresql+psycopg2://docket:docket@localhost:5432"

# Database name to create
DB_NAME = "docket_db"

# Full URL including the database name
DB_URL = f"{DATABASE_URL}/{DB_NAME}"

# Connect to the server without specifying the database name
engine = create_engine(DATABASE_URL)

# Check if the database exists, and create it if it doesn't
if not database_exists(DB_URL):
    create_database(DB_URL)
    print(f"Database '{DB_NAME}' created successfully.")
else:
    print(f"Database '{DB_NAME}' already exists.")
