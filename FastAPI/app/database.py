# ============================================
# DATABASE CONFIGURATION
# ============================================
# This file contains the database setup using SQLAlchemy
# SQLAlchemy is an ORM (Object Relational Mapping) that helps us interact with databases using Python objects

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Define the database URL
# SQLite is a lightweight, file-based database perfect for learning and small projects
# The database file will be stored in 'ecommerce.db'
DATABASE_URL = "sqlite:///./ecommerce.db"

# Create the database engine
# The engine is the starting point for all SQLAlchemy applications
# It manages connections to the database
engine = create_engine(
    DATABASE_URL,
    # connect_args is used for SQLite to handle threading
    connect_args={"check_same_thread": False}
)

# Create a session factory
# Sessions are used to interact with the database (like ORM queries)
# SessionLocal() is what we use in our endpoints to get a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models
# All database models will inherit from this Base class
Base = declarative_base()

# Dependency function
# This is used in FastAPI endpoints to get a database session
def get_db():
    """
    Get a database session for use in API endpoints.
    This is a generator function (uses 'yield' instead of 'return').
    
    How it works:
    1. Creates a new database session
    2. Yields it to the endpoint (the endpoint uses it)
    3. Ensures the session is closed after the endpoint finishes (finally block)
    
    Usage in endpoint:
    @app.get('/products')
    def get_products(db: Session = Depends(get_db)):
        # Use db to query database
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
