from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Database connection URL
DATABASE_URL = "postgresql+psycopg2://docket:docket@localhost:5432/docket_db"
engine = create_engine(DATABASE_URL)

# Use the new import path for declarative_base
Base = declarative_base()

# Define models
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship to Orders
    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship to OrderItems
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'

    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")


# === For Docket App === # 
"""
    1 - Workspace => M - Workflows 
    1 - Workflow => M - WorflowRuns
    1 - WorkflowRun => M - WorkflowRunLogs
"""
class WorkflowState:
    # Enum of Workflow State
    pass


class Workspace(Base):
    __tablename__ = 'workspace'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    location = Column(String(50), nullable=False)
    logs_bucket = Column(String(50), nullable=False)
    url = Column(String(50), nullable=False)
    added_dt = Column(DateTime, server_default=func.now())
    # Add a one-to-many relationship to Workflow
    workflows = relationship("Workflow", back_populates="workspace")
    

class Workflow(Base):
    __tablename__ = 'workflow'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    description = Column(String)
    state = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_dt = Column(DateTime, server_default=func.now())
    published_dt = Column(DateTime)
    archived_dt = Column(DateTime)
    version = Column(Integer, nullable=False)
    git_repo_url = Column(String(50), nullable=False)
    git_branch = Column(String(50), nullable=False)
    git_commit_id = Column(String(50), nullable=False)
    workspace_id = Column(Integer, ForeignKey('workspace.id'), nullable=False)  
    test = Column(String(50))  
    # Relationships
    workspace = relationship("Workspace", back_populates="workflows")
    workflow_runs = relationship("WorkflowRun", back_populates="workflow")
    

class WorkflowRun(Base):
    __tablename__ = 'workflow_run'
    id = Column(Integer, primary_key=True, unique=True)
    run_id = Column(String(50), nullable=False)
    start_dt = Column(DateTime, server_default=func.now())
    end_dt = Column(DateTime)
    killed_dt = Column(DateTime)
    status = Column(String(50), nullable=False)
    submitted_by = Column(String(50), nullable=False)
    workflow_id = Column(Integer, ForeignKey('workflow.id'), nullable=False)
    # Relationships
    workflow = relationship("Workflow", back_populates="workflow_runs")
    workflow_run_logs = relationship("WorkflowRunLog", back_populates="workflow_run")
    

class WorkflowRunLog(Base):
    """
    A Task will have multiple entries over lifetime of execution. 
    """
    __tablename__ = 'workflow_run_log'
    id = Column(Integer, primary_key=True, unique=True)
    task_name = Column(String(50), nullable=False)
    task_id = Column(String(50), nullable=False)
    task_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    entry_dt = Column(DateTime, server_default=func.now())
    workflow_run_id = Column(Integer, ForeignKey('workflow_run.id'), nullable=False)
    # Relationships
    workflow_run = relationship("WorkflowRun", back_populates="workflow_run_logs")
    

if __name__ == "__main__":
    # Create the tables in the database
    Base.metadata.create_all(engine)
    
    # 
    # drop table workflow_run_log;drop table workflow_run;drop table workflow;drop table workspace;

    # Set up the session
    Session = sessionmaker(bind=engine)
    session = Session()
