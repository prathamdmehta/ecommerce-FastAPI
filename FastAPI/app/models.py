# ============================================
# DATABASE MODELS (SQLAlchemy ORM Models)
# ============================================
# These are Python classes that represent database tables
# Each class = one database table
# Each attribute = one column in the table

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# ===== MODEL 1: User Model =====
class User(Base):
    """
    Represents a user in the ecommerce system.
    This table stores user information for authentication and profiling.
    
    Attributes:
        id: Unique identifier for each user (Primary Key)
        email: User's email address (must be unique)
        username: User's username (must be unique)
        password_hash: Encrypted password (never store plain passwords!)
        is_active: Whether the user account is active
        created_at: When the user registered
        orders: Relationship to Order model (one user can have multiple orders)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship: One user can have many orders
    orders = relationship("Order", back_populates="user")

# ===== MODEL 2: Product Model =====
class Product(Base):
    """
    Represents a product in the ecommerce store.
    
    Attributes:
        id: Unique product identifier (Primary Key)
        name: Product name
        description: Detailed product description
        price: Product price
        currency: Currency of the price (e.g., USD, EUR)
        color: Product color
        image: URL to product image
        stock: Number of items in stock
        rating: Average product rating (1-5)
        category_id: Foreign key to Category (which category this product belongs to)
        created_at: When the product was added
        category: Relationship to Category model
        order_items: Relationship to OrderItem model (this product in various orders)
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    currency = Column(String, default="USD")
    color = Column(String)
    image = Column(String)
    stock = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship: A product belongs to one category
    category = relationship("Category", back_populates="products")
    # Relationship: A product can be in many orders
    order_items = relationship("OrderItem", back_populates="product")

# ===== MODEL 3: Category Model =====
class Category(Base):
    """
    Represents a product category.
    Categories help organize products (e.g., Books, Electronics, Clothing)
    
    Attributes:
        id: Unique category identifier
        name: Category name
        description: Category description
        image: Category image/icon URL
        products: Relationship to Product model (one category has many products)
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    image = Column(String)
    
    # Relationship: One category can have many products
    products = relationship("Product", back_populates="category")

# ===== MODEL 4: Order Model =====
class Order(Base):
    """
    Represents a customer order.
    An order contains multiple products (via OrderItem).
    
    Attributes:
        id: Unique order identifier
        user_id: Foreign key to User (who made this order)
        total_price: Total cost of the order
        status: Order status (pending, completed, cancelled)
        created_at: When the order was placed
        user: Relationship to User model
        items: Relationship to OrderItem model (products in this order)
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship: An order belongs to one user
    user = relationship("User", back_populates="orders")
    # Relationship: An order contains many items (products)
    items = relationship("OrderItem", back_populates="order")

# ===== MODEL 5: OrderItem Model =====
class OrderItem(Base):
    """
    Represents a single item (product) in an order.
    This is a "junction table" that connects Orders and Products.
    
    Example: If a customer orders 3 products, there will be 3 OrderItem rows.
    
    Attributes:
        id: Unique item identifier
        order_id: Foreign key to Order
        product_id: Foreign key to Product
        quantity: How many of this product in the order
        price: Price per unit at time of purchase
        order: Relationship to Order model
        product: Relationship to Product model
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    price = Column(Float)  # Price at time of purchase (might differ from current product price)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
