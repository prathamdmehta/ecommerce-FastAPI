# ============================================
# PYDANTIC SCHEMAS (Request/Response Validation)
# ============================================
# Schemas define what data we expect from users and what we return
# Pydantic automatically validates data types and structure
# If data doesn't match the schema, it returns a validation error

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ===== CATEGORY SCHEMAS =====

class CategoryBase(BaseModel):
    """Base schema for category - contains shared fields"""
    name: str = Field(..., min_length=1, max_length=50, description="Category name")
    description: Optional[str] = Field(None, max_length=500, description="Category description")
    image: Optional[str] = Field(None, description="Category image URL")

class CategoryCreate(CategoryBase):
    """Schema for creating a new category (POST request)"""
    pass

class CategoryUpdate(BaseModel):
    """Schema for updating a category (PUT request) - all fields are optional"""
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

class Category(CategoryBase):
    """Schema for returning a category (database object)"""
    id: int
    
    class Config:
        from_attributes = True  # Allow creating Pydantic model from SQLAlchemy model

# ===== PRODUCT SCHEMAS =====

class ProductBase(BaseModel):
    """Base schema for product"""
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    description: Optional[str] = Field(None, max_length=1000, description="Product description")
    price: float = Field(..., gt=0, description="Product price (must be > 0)")
    currency: str = Field(default="USD", description="Currency code")
    color: Optional[str] = Field(None, max_length=50, description="Product color")
    image: Optional[str] = Field(None, description="Product image URL")
    stock: int = Field(default=0, ge=0, description="Stock quantity (must be >= 0)")
    rating: float = Field(default=0.0, ge=0, le=5, description="Rating from 0-5")
    category_id: int = Field(..., description="ID of the category")

class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    pass

class ProductUpdate(BaseModel):
    """Schema for updating a product - all fields optional"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    color: Optional[str] = None
    image: Optional[str] = None
    stock: Optional[int] = None
    rating: Optional[float] = None
    category_id: Optional[int] = None

class Product(ProductBase):
    """Schema for returning a product"""
    id: int
    created_at: datetime
    category: Category  # Include category information
    
    class Config:
        from_attributes = True

class ProductWithoutCategory(ProductBase):
    """Product schema without category (to avoid circular references)"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ===== USER SCHEMAS =====

class UserBase(BaseModel):
    """Base schema for user"""
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")

class UserCreate(UserBase):
    """Schema for creating a new user (registration)"""
    password: str = Field(..., min_length=6, max_length=100, description="Password (min 6 chars)")

class UserUpdate(BaseModel):
    """Schema for updating user info"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class User(UserBase):
    """Schema for returning user info"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserWithOrders(User):
    """User schema including their orders"""
    orders: List['Order'] = []

# ===== ORDER ITEM SCHEMAS =====

class OrderItemBase(BaseModel):
    """Base schema for order item"""
    product_id: int = Field(..., description="ID of the product")
    quantity: int = Field(..., gt=0, description="Quantity (must be > 0)")

class OrderItemCreate(OrderItemBase):
    """Schema for adding item to order"""
    pass

class OrderItem(OrderItemBase):
    """Schema for returning order item"""
    id: int
    price: float  # Price at purchase time
    product: ProductWithoutCategory
    
    class Config:
        from_attributes = True

# ===== ORDER SCHEMAS =====

class OrderCreate(BaseModel):
    """Schema for creating a new order"""
    items: List[OrderItemCreate] = Field(..., min_items=1, description="At least one item required")

class OrderUpdate(BaseModel):
    """Schema for updating order status"""
    status: str = Field(..., description="Order status: pending, completed, cancelled")

class Order(BaseModel):
    """Schema for returning an order"""
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItem] = []
    
    class Config:
        from_attributes = True

class OrderDetail(Order):
    """Order with user information"""
    user: User

# ===== AUTH SCHEMAS =====

class Token(BaseModel):
    """Schema for login response (JWT token)"""
    access_token: str
    token_type: str = "bearer"
    user: User

class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[int] = None
    email: Optional[str] = None

class LoginRequest(BaseModel):
    """Schema for login request"""
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")

# ===== RESPONSE SCHEMAS =====

class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    """Generic error response"""
    success: bool = False
    message: str
    detail: Optional[str] = None
