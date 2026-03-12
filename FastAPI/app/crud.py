# ============================================
# CRUD OPERATIONS (Create, Read, Update, Delete)
# ============================================
# These are reusable functions to interact with the database
# Instead of writing the same database logic in every endpoint,
# we centralize it here and reuse it

from sqlalchemy.orm import Session
from models import Product, Category, User, Order, OrderItem
from schemas import ProductCreate, ProductUpdate, CategoryCreate, CategoryUpdate, OrderCreate
from datetime import datetime

# ===================================
# PRODUCT CRUD OPERATIONS
# ===================================

def get_products(db: Session, skip: int = 0, limit: int = 100):
    """
    Get all products with pagination.
    
    Args:
        db: Database session
        skip: Number of products to skip (for pagination)
        limit: Maximum number of products to return
    
    Returns:
        List of Product objects
    """
    return db.query(Product).offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int):
    """
    Get a single product by ID.
    
    Args:
        db: Database session
        product_id: The product ID to search for
    
    Returns:
        Product object if found, None otherwise
    """
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_name(db: Session, name: str):
    """Get products by name (case-insensitive search)"""
    return db.query(Product).filter(
        Product.name.ilike(f"%{name}%")
    ).all()

def create_product(db: Session, product: ProductCreate):
    """
    Create a new product in the database.
    
    Args:
        db: Database session
        product: ProductCreate schema with product data
    
    Returns:
        The newly created Product object
    
    Process:
        1. Convert Pydantic schema to SQLAlchemy model
        2. Add to database session
        3. Commit changes
        4. Refresh to get database-generated values (like ID)
        5. Return the created product
    """
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: ProductUpdate):
    """
    Update an existing product.
    
    Args:
        db: Database session
        product_id: ID of product to update
        product_update: ProductUpdate schema with new data
    
    Returns:
        Updated Product object, or None if not found
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None
    
    # Update only provided fields
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    """
    Delete a product from the database.
    
    Args:
        db: Database session
        product_id: ID of product to delete
    
    Returns:
        True if deleted, False if not found
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return False
    
    db.delete(db_product)
    db.commit()
    return True

# ===================================
# CATEGORY CRUD OPERATIONS
# ===================================

def get_categories(db: Session):
    """Get all categories"""
    return db.query(Category).all()

def get_category_by_id(db: Session, category_id: int):
    """Get a category by ID"""
    return db.query(Category).filter(Category.id == category_id).first()

def create_category(db: Session, category: CategoryCreate):
    """Create a new category"""
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_update: CategoryUpdate):
    """Update an existing category"""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    """Delete a category"""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return False
    
    db.delete(db_category)
    db.commit()
    return True

# ===================================
# ORDER CRUD OPERATIONS
# ===================================

def create_order(db: Session, user_id: int, order: OrderCreate):
    """
    Create a new order with multiple items.
    
    Args:
        db: Database session
        user_id: ID of user placing the order
        order: OrderCreate schema with items
    
    Returns:
        The created Order object
    
    Process:
        1. Calculate total price by checking each product
        2. Create Order object
        3. For each item, create OrderItem and link to order
        4. Commit all changes
    """
    # Calculate total price
    total_price = 0
    order_items = []
    
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise ValueError(f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise ValueError(f"Insufficient stock for product {product.name}")
        
        total_price += product.price * item.quantity
        order_items.append((product, item.quantity))
    
    # Create the order
    db_order = Order(user_id=user_id, total_price=total_price)
    db.add(db_order)
    db.flush()  # Flush to get the order ID without committing
    
    # Add items to the order
    for product, quantity in order_items:
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=product.id,
            quantity=quantity,
            price=product.price
        )
        db.add(db_order_item)
        # Decrease product stock
        product.stock -= quantity
    
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order_by_id(db: Session, order_id: int):
    """Get an order by ID"""
    return db.query(Order).filter(Order.id == order_id).first()

def get_user_orders(db: Session, user_id: int):
    """Get all orders for a specific user"""
    return db.query(Order).filter(Order.user_id == user_id).all()

def update_order_status(db: Session, order_id: int, status: str):
    """Update the status of an order"""
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return None
    
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order

def cancel_order(db: Session, order_id: int):
    """
    Cancel an order and restore product stock.
    
    Args:
        db: Database session
        order_id: ID of order to cancel
    
    Returns:
        The updated Order object
    """
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return None
    
    if db_order.status == "completed":
        raise ValueError("Cannot cancel a completed order")
    
    # Restore stock for all items in the order
    for item in db_order.items:
        item.product.stock += item.quantity
    
    db_order.status = "cancelled"
    db.commit()
    db.refresh(db_order)
    return db_order
