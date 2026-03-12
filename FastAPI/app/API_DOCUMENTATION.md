# FastAPI Ecommerce API - Complete Documentation

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [API Endpoints](#api-endpoints)
4. [Authentication](#authentication)
5. [Database Models](#database-models)
6. [Running the Application](#running-the-application)
7. [Testing the API](#testing-the-api)
8. [Common Issues](#common-issues)
9. [FastAPI Concepts Explained](#fastapi-concepts-explained)

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install JWT library (if not in requirements):**
```bash
pip install python-jose python-multipart
```

3. **Create .env file in the app directory:**
```
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=sqlite:///./ecommerce.db
```

### Quick Start

1. **Navigate to the app directory:**
```bash
cd FastAPI/app
```

2. **Run the application:**
```bash
uvicorn main_new:app --reload
```

3. **Access the API:**
- API Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- Health Check: http://localhost:8000/health

---

## Project Structure

```
FastAPI/
├── app/
│   ├── main_new.py           # Main application file (refactored)
│   ├── main.py               # Original file (kept for reference)
│   ├── database.py           # Database configuration
│   ├── models.py             # SQLAlchemy ORM models
│   ├── schemas.py            # Pydantic validation schemas
│   ├── crud.py               # Database CRUD operations
│   ├── auth.py               # Password hashing & JWT tokens
│   ├── service/
│   │   ├── products.py       # Original product service
│   │   └── __pycache__/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── products.py       # Product endpoints
│   │   ├── categories.py     # Category endpoints
│   │   └── orders.py         # Order endpoints
│   ├── data/
│   │   └── products.json     # Original product data
│   ├── ecommerce.db          # SQLite database (auto-created)
│   └── __pycache__/
└── requirements.txt          # Python dependencies
```

---

## API Endpoints

### Base URL
```
http://localhost:8000/api/v1
```

### Health Endpoints

#### Check API Health
```
GET /health
```

Response:
```json
{
  "status": "healthy"
}
```

---

### Authentication Endpoints

#### Register New User
```
POST /api/v1/auth/register
```

Request Body:
```json
{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "securepassword123"
}
```

Response (201 Created):
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "is_active": true,
  "created_at": "2024-01-20T10:30:00"
}
```

#### Login
```
POST /api/v1/auth/login
```

Request Body:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "john_doe",
    "is_active": true,
    "created_at": "2024-01-20T10:30:00"
  }
}
```

---

### Category Endpoints

#### Get All Categories
```
GET /api/v1/categories
```

Response:
```json
[
  {
    "id": 1,
    "name": "Electronics",
    "description": "Electronic devices",
    "image": "url-to-image"
  }
]
```

#### Get Category by ID
```
GET /api/v1/categories/{category_id}
```

#### Create Category
```
POST /api/v1/categories
```

Request Body:
```json
{
  "name": "Laptops",
  "description": "Portable computers",
  "image": "url-to-image"
}
```

#### Update Category
```
PUT /api/v1/categories/{category_id}
```

Request Body (all fields optional):
```json
{
  "name": "Updated Name",
  "description": "Updated description"
}
```

#### Delete Category
```
DELETE /api/v1/categories/{category_id}
```

---

### Product Endpoints

#### Get All Products
```
GET /api/v1/products
```

Query Parameters:
- `skip` (int): Number of products to skip (default: 0)
- `limit` (int): Maximum products to return (default: 10, max: 100)
- `name` (string): Filter by product name
- `sort_by_price` (bool): Sort by price
- `order` (string): Sort order - 'asc' or 'desc'

Examples:
```
GET /api/v1/products
GET /api/v1/products?skip=10&limit=20
GET /api/v1/products?name=keyboard
GET /api/v1/products?sort_by_price=true&order=desc
```

Response:
```json
{
  "total": 100,
  "items": [
    {
      "id": 1,
      "name": "Laptop",
      "description": "High performance laptop",
      "price": 999.99,
      "currency": "USD",
      "color": "Silver",
      "image": "url",
      "stock": 50,
      "rating": 4.5,
      "category_id": 1,
      "created_at": "2024-01-20T10:30:00",
      "category": {...}
    }
  ],
  "skip": 0,
  "limit": 10
}
```

#### Get Product by ID
```
GET /api/v1/products/{product_id}
```

#### Create Product
```
POST /api/v1/products
```

Request Body:
```json
{
  "name": "Laptop",
  "description": "High performance laptop",
  "price": 999.99,
  "currency": "USD",
  "color": "Silver",
  "image": "url",
  "stock": 50,
  "rating": 4.5,
  "category_id": 1
}
```

#### Update Product
```
PUT /api/v1/products/{product_id}
```

Request Body (all fields optional):
```json
{
  "price": 1099.99,
  "stock": 40
}
```

#### Delete Product
```
DELETE /api/v1/products/{product_id}
```

---

### Order Endpoints

#### Create Order
```
POST /api/v1/orders?user_id=1
```

Request Body:
```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ]
}
```

Response (201 Created):
```json
{
  "id": 1,
  "user_id": 1,
  "total_price": 2099.97,
  "status": "pending",
  "created_at": "2024-01-20T10:30:00",
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "quantity": 2,
      "price": 999.99,
      "product": {...}
    }
  ]
}
```

#### Get Order by ID
```
GET /api/v1/orders/{order_id}
```

#### Get User's Orders
```
GET /api/v1/orders/user/{user_id}
```

#### Update Order Status
```
PUT /api/v1/orders/{order_id}/status
```

Request Body:
```json
{
  "status": "completed"
}
```

Valid Statuses: `pending`, `processing`, `shipped`, `completed`, `cancelled`

#### Cancel Order
```
POST /api/v1/orders/{order_id}/cancel
```

---

## Authentication

### How JWT Auth Works

1. **User registers/logs in** → Server returns access token
2. **Client stores token** → Usually in localStorage
3. **Client includes token in requests** → In Authorization header
4. **Server verifies token** → Validates and extracts user data

### Using the Token

Include the token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

Example using curl:
```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  http://localhost:8000/api/v1/orders/1
```

### Token Expiration
Tokens expire after 30 minutes. Users need to login again to get a new token.

---

## Database Models

### User Model
Stores user account information.

Fields:
- `id` (int): Primary key
- `email` (string): Unique email
- `username` (string): Unique username
- `password_hash` (string): Encrypted password
- `is_active` (bool): Account status
- `created_at` (datetime): Registration date

### Category Model
Product categories for organization.

Fields:
- `id` (int): Primary key
- `name` (string): Unique category name
- `description` (string): Category description
- `image` (string): Category image URL

### Product Model
Physical products for sale.

Fields:
- `id` (int): Primary key
- `name` (string): Product name
- `description` (string): Full description
- `price` (float): Product price
- `currency` (string): Price currency
- `color` (string): Product color
- `image` (string): Product image URL
- `stock` (int): Available quantity
- `rating` (float): Average rating (0-5)
- `category_id` (int): Foreign key to Category
- `created_at` (datetime): Creation date

### Order Model
Customer orders.

Fields:
- `id` (int): Primary key
- `user_id` (int): Foreign key to User
- `total_price` (float): Order total
- `status` (string): Order status
- `created_at` (datetime): Order date

### OrderItem Model
Individual items in an order.

Fields:
- `id` (int): Primary key
- `order_id` (int): Foreign key to Order
- `product_id` (int): Foreign key to Product
- `quantity` (int): Number of units
- `price` (float): Price per unit at purchase time

---

## Running the Application

### Development Mode (with auto-reload)
```bash
cd FastAPI/app
uvicorn main_new:app --reload
```

### Production Mode (without auto-reload)
```bash
cd FastAPI/app
uvicorn main_new:app --host 0.0.0.0 --port 8000
```

### Using Python directly
```bash
cd FastAPI/app
python main_new.py
```

---

## Testing the API

### Using Swagger UI
1. Go to http://localhost:8000/api/docs
2. Click on an endpoint to expand it
3. Click "Try it out"
4. Fill in parameters and request body
5. Click "Execute"

### Using curl

#### Get all products:
```bash
curl http://localhost:8000/api/v1/products
```

#### Register user:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

#### Login:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

---

## Common Issues

### Issue: "No module named 'fastapi'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Database is locked"
**Solution:** SQLite doesn't handle concurrent writes well. Either:
1. Close other connections
2. Use PostgreSQL for production

### Issue: "Port 8000 already in use"
**Solution:** Use a different port
```bash
uvicorn main_new:app --port 8001
```

### Issue: "CORS error"
**Solution:** Already configured in main.py. If issues persist, check allowed origins.

---

## FastAPI Concepts Explained

### 1. **FastAPI Basics**

#### What is FastAPI?
FastAPI is a modern Python framework for building web APIs quickly. It uses:
- **Python type hints** for automatic validation
- **Pydantic** for data validation
- **Starlette** for routing and middleware
- **uvicorn** as the ASGI server

#### Simple Endpoint
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

**@app.get()** decorator:
- Creates a GET endpoint
- URL: `/`
- Automatically converts return value to JSON

---

### 2. **Path Parameters**

Path parameters are part of the URL.

```python
@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {"product_id": product_id}
```

URL: `/products/5`
Response: `{"product_id": 5}`

**Type Hint (int):** FastAPI automatically:
1. Converts "5" (string) to 5 (int)
2. Validates it's a number
3. Returns error if not: "value is not a valid integer"

---

### 3. **Query Parameters**

Query parameters come after `?` in the URL.

```python
@app.get("/search")
def search_products(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

Usage:
- `/search` → skip=0, limit=10 (defaults)
- `/search?skip=20&limit=5` → skip=20, limit=5

---

### 4. **Request Body (POST/PUT)**

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    description: str = None  # Optional

@app.post("/products")
def create_product(product: Product):
    return {"created": product}
```

Request:
```json
{
  "name": "Laptop",
  "price": 999.99,
  "description": "High performance"
}
```

Response:
```json
{
  "created": {
    "name": "Laptop",
    "price": 999.99,
    "description": "High performance"
  }
}
```

---

### 5. **Pydantic Schemas**

Pydantic validates data automatically.

```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr  # Validates email format
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)  # ... means required
```

Automatic validation:
- Invalid email → Error
- Username too short → Error
- Password missing → Error

---

### 6. **HTTP Status Codes**

```python
@app.post("/products", status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.create_product(db, product)
    return db_product
```

Common status codes:
- `200` OK - Request successful
- `201` Created - New resource created
- `400` Bad Request - Invalid input
- `401` Unauthorized - Not authenticated
- `404` Not Found - Resource doesn't exist
- `500` Server Error - Server problem

---

### 7. **Dependency Injection**

Dependency Injection allows sharing reusable components.

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
```

Benefits:
- Automatically manages database connections
- Testable (can inject mock DB)
- Reusable across endpoints

---

### 8. **HTTPException**

For returning errors with status codes:

```python
from fastapi import HTTPException

@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product
```

Response (404):
```json
{
  "detail": "Product not found"
}
```

---

### 9. **CRUD Operations**

CRUD = Create, Read, Update, Delete

```python
# CREATE
def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# READ
def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

# UPDATE
def update_product(db: Session, product_id: int, product_update):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    for field, value in product_update.dict().items():
        setattr(db_product, field, value)
    db.commit()
    return db_product

# DELETE
def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
```

---

### 10. **Routers (Organizing Code)**

Group related endpoints using routers:

```python
# routes/products.py
from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def list_products():
    pass

@router.post("/")
def create_product():
    pass

# main.py
from routes import products

app.include_router(products.router, prefix="/api/v1")
```

Result:
- `GET /api/v1/products/`
- `POST /api/v1/products/`

---

### 11. **SQLAlchemy ORM**

ORM = Object-Relational Mapping (interact with DB using Python objects)

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

# Create table
engine = create_engine("sqlite:///./test.db")
Base.metadata.create_all(bind=engine)

# Use in endpoint
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products
```

---

### 12. **JWT Authentication**

JWT = JSON Web Token (secure way to pass user info)

**How it works:**
1. User logs in → Server creates token
2. Client stores token
3. Client sends token in Authorization header
4. Server verifies token → Extract user data

```python
from jose import jwt
from datetime import datetime, timedelta

# Create token
def create_access_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, "secret_key", algorithm="HS256")
    return token

# Verify token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, "secret_key", algorithms=["HS256"])
        return payload
    except:
        return None
```

---

### 13. **Response Models**

Define and validate API responses:

```python
class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    
    class Config:
        from_attributes = True  # Convert SQLAlchemy model to Pydantic

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    # Returns response formatted according to ProductResponse schema
    pass
```

Benefits:
- Automatic response serialization
- API documentation with correct format
- IDE autocomplete

---

### 14. **Error Handling**

```python
from fastapi import HTTPException

try:
    product = db.query(Product).filter(Product.id == 1).first()
    if not product:
        raise HTTPException(404, "Product not found")
    return product
except Exception as e:
    raise HTTPException(500, f"Server error: {str(e)}")
```

---

### 15. **CORS (Cross-Origin Resource Sharing)**

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
```

Allows frontend on different domain/port to access your API.

---

## Summary

You now have a complete, production-ready ecommerce API with:
- ✅ User authentication (JWT)
- ✅ Product management
- ✅ Order processing
- ✅ Database with relationships
- ✅ Proper error handling
- ✅ API documentation
- ✅ Clean code structure

### Next Steps
1. Run the application
2. Explore endpoints in Swagger UI
3. Test API locally
4. Read through the code and comments
5. Extend with more features!

Happy coding! 🚀
