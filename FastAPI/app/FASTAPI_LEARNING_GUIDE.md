# FastAPI Complete Learning Guide

## 📖 Master FastAPI in 30 Minutes

This guide explains every important FastAPI concept with examples. Read through carefully!

---

## Table of Contents

1. [What is FastAPI?](#what-is-fastapi)
2. [Installation & Setup](#installation--setup)
3. [Basic Concepts](#basic-concepts)
4. [Request Handling](#request-handling)
5. [Response Handling](#response-handling)
6. [Data Validation](#data-validation)
7. [Dependency Injection](#dependency-injection)
8. [Error Handling](#error-handling)
9. [Authentication](#authentication)
10. [Database Integration](#database-integration)
11. [Code Organization](#code-organization)
12. [Advanced Topics](#advanced-topics)

---

## What is FastAPI?

### FastAPI Definition
**FastAPI** is a modern Python web framework for building REST APIs (Application Programming Interfaces) with:
- **High performance** - Among the fastest Python frameworks
- **Easy to use** - Less code, fewer bugs
- **Quick to learn** - Intuitive syntax
- **Built-in validation** - Automatic request/response validation
- **Auto documentation** - Swagger UI & ReDoc docs generated automatically

### Why Use FastAPI?

| Feature | Benefit |
|---------|---------|
| Type hints | Python validates types automatically |
| Pydantic | Powerful data validation |
| Starlette | Fast ASGI framework underneath |
| OpenAPI | Auto-generated API documentation |
| Development | 40-60% less code than Flask/Django |

### FastAPI vs Alternatives

```
FastAPI:     🚀 FASTEST, type hints, auto docs
Django:      🐢 SLOWER, batteries-included, ORM
Flask:       🚶 SLOWER, minimal, manual everything
```

---

## Installation & Setup

### 1. Install FastAPI and Uvicorn

```bash
pip install fastapi uvicorn[standard]
```

**What's uvicorn?**
- ASGI server that runs FastAPI
- Similar to how Apache runs PHP
- Handles HTTP requests and sends responses

### 2. Create Your First API

**File: main.py**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    """Welcome endpoint"""
    return {"message": "Hello World"}
```

### 3. Run the Server

```bash
uvicorn main:app --reload
```

Output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 4. Test the API

- Open browser: http://localhost:8000/
- See response: `{"message": "Hello World"}`
- Auto-docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Basic Concepts

### 1. HTTP Methods

FastAPI endpoints use HTTP methods to define what operation to perform:

| Method | Operation | Example |
|--------|-----------|---------|
| GET | Read data | `/products/1` → Get product 1 |
| POST | Create data | `/products` → Create new product |
| PUT | Update data | `/products/1` → Replace product 1 |
| PATCH | Partial update | `/products/1` → Update some fields |
| DELETE | Delete data | `/products/1` → Delete product 1 |

### 2. Creating Endpoints

```python
from fastapi import FastAPI

app = FastAPI()

# GET endpoint
@app.get("/products")
def get_products():
    """Get all products"""
    return [
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Phone"}
    ]

# POST endpoint
@app.post("/products")
def create_product():
    """Create a new product"""
    return {"id": 3, "name": "Tablet"}

# PUT endpoint
@app.put("/products/1")
def update_product():
    """Update a product"""
    return {"id": 1, "name": "Updated Laptop"}

# DELETE endpoint
@app.delete("/products/1")
def delete_product():
    """Delete a product"""
    return {"message": "Product deleted"}
```

### 3. Status Codes

```python
@app.post("/products", status_code=201)
def create_product():
    """
    Returns 201 Created instead of default 200 OK
    """
    return {"id": 3, "name": "New Product"}

# Common status codes:
# 200 - OK (success)
# 201 - Created (new resource created)
# 204 - No Content (success, no response body)
# 400 - Bad Request (invalid input)
# 401 - Unauthorized (not authenticated)
# 403 - Forbidden (authenticated but no permission)
# 404 - Not Found (resource doesn't exist)
# 500 - Internal Server Error (server error)
```

---

## Request Handling

### 1. Path Parameters

Path parameters are **part of the URL** and required.

```python
@app.get("/products/{product_id}")
def get_product(product_id: int):
    """Get a product by ID"""
    return {"product_id": product_id, "name": f"Product {product_id}"}
```

**How it works:**
- URL: `/products/5`
- FastAPI extracts: `product_id = 5` (as integer)
- Type hint `int` = automatic validation

**If user passes non-integer:**
- URL: `/products/hello`
- FastAPI returns error: `"value is not a valid integer"`

### 2. Multiple Path Parameters

```python
@app.get("/categories/{category_id}/products/{product_id}")
def get_category_product(category_id: int, product_id: int):
    return {
        "category_id": category_id,
        "product_id": product_id
    }
```

URL: `/categories/1/products/5`
Response: `{"category_id": 1, "product_id": 5}`

### 3. Query Parameters

Query parameters come **after `?` in the URL** and are optional.

```python
@app.get("/products")
def search_products(skip: int = 0, limit: int = 10):
    """
    skip: Number of products to skip (default: 0)
    limit: Number of products to return (default: 10)
    """
    return {
        "skip": skip,
        "limit": limit,
        "data": []
    }
```

**Usage Examples:**
- `/products` → skip=0, limit=10
- `/products?skip=20` → skip=20, limit=10
- `/products?limit=5` → skip=0, limit=5
- `/products?skip=20&limit=5` → skip=20, limit=5

### 4. Query Parameter Validation

```python
from fastapi import Query

@app.get("/products")
def get_products(
    skip: int = Query(0, ge=0),  # ≥ 0
    limit: int = Query(10, ge=1, le=100)  # 1-100
):
    """
    ge = greater than or equal
    le = less than or equal
    """
    return {"skip": skip, "limit": limit}
```

**Validation:**
- `/products?skip=-5` → Error: "ensure this value is greater than or equal to 0"
- `/products?limit=200` → Error: "ensure this value is less than or equal to 100"

### 5. Request Body (JSON)

Request body is sent as **JSON** in POST/PUT requests.

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    description: str = None  # Optional field

@app.post("/products")
def create_product(product: Product):
    """
    Expects JSON:
    {
        "name": "Laptop",
        "price": 999.99,
        "description": "High performance"
    }
    """
    return {"created": product}
```

**What happens:**
1. User sends JSON: `{"name": "Laptop", "price": 999.99}`
2. FastAPI validates it matches `Product` schema
3. Converts JSON to Python object: `product.name = "Laptop"`
4. Passes to function

**Invalid request handling:**
- Missing required field → Error
- Wrong type → Error
- Extra fields → Ignored (by default)

### 6. Combining Parameters

```python
@app.post("/categories/{category_id}/products")
def create_category_product(
    category_id: int,  # Path parameter (required)
    product: Product,  # Request body
    rating: float = Query(None, ge=0, le=5)  # Query parameter (optional)
):
    """Combines all three"""
    return {
        "category_id": category_id,
        "product": product,
        "rating": rating
    }
```

URL: `/categories/1/products?rating=4.5`
Body:
```json
{
    "name": "Laptop",
    "price": 999.99
}
```

Response:
```json
{
    "category_id": 1,
    "product": {"name": "Laptop", "price": 999.99},
    "rating": 4.5
}
```

---

## Response Handling

### 1. Basic Responses

```python
# Returns Python dict → FastAPI converts to JSON
@app.get("/products/1")
def get_product():
    return {
        "id": 1,
        "name": "Laptop",
        "price": 999.99
    }
```

Response:
```json
{
    "id": 1,
    "name": "Laptop",
    "price": 999.99
}
```

### 2. Response Models

Define expected response structure:

```python
from pydantic import BaseModel

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

@app.get("/products/1", response_model=ProductResponse)
def get_product():
    return {
        "id": 1,
        "name": "Laptop",
        "price": 999.99,
        "internal_data": "hidden"  # Not included in response
    }
```

**Benefits:**
- API documentation shows correct response format
- Fields not in model are excluded
- Type validation on response
- IDE autocomplete for responses

### 3. List Responses

```python
from typing import List

class Product(BaseModel):
    id: int
    name: str

@app.get("/products", response_model=List[Product])
def get_products():
    return [
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Phone"}
    ]
```

### 4. Custom Status Codes

```python
@app.post("/products", status_code=201)
def create_product():
    return {"id": 1, "name": "New Product"}

# Response: 201 Created (instead of default 200 OK)
```

---

## Data Validation

### 1. Pydantic Basics

Pydantic automatically validates data:

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str  # Must be string
    price: float  # Must be number
    stock: int = 0  # Default to 0

# Valid
product = Product(name="Laptop", price=999.99)

# Invalid - Wrong type
try:
    product = Product(name="Laptop", price="expensive")  # String, not float
except Exception as e:
    print(e)  # "value is not a valid float"
```

### 2. Field Validation

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)  # ... = required
    price: float = Field(..., gt=0)  # gt = greater than
    stock: int = Field(default=0, ge=0)  # ge = greater than or equal
    rating: float = Field(default=0, ge=0, le=5)  # le = less than or equal

# Valid
p = Product(name="Laptop", price=999.99)

# Invalid - name too long
try:
    p = Product(name="A" * 101, price=999.99)
except Exception as e:
    print(e)  # "ensure this value has at most 100 characters"
```

### 3. Optional Fields

```python
from typing import Optional

class Product(BaseModel):
    name: str  # Required
    description: Optional[str] = None  # Optional
    image_url: Optional[str] = Field(None, description="Product image")

# Valid - all
p = Product(name="Laptop", description="Fast laptop", image_url="...")

# Valid - only required
p = Product(name="Laptop")

# Invalid - no name
try:
    p = Product()
except Exception as e:
    print(e)  # "field required"
```

### 4. Custom Validation

```python
from pydantic import BaseModel, field_validator

class Product(BaseModel):
    name: str
    price: float
    
    @field_validator('name')
    def name_cannot_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v

# Invalid - empty name
try:
    p = Product(name="   ", price=999.99)
except Exception as e:
    print(e)  # "Name cannot be empty"
```

### 5. Email Validation

```python
from pydantic import EmailStr

class User(BaseModel):
    email: EmailStr  # Automatically validates email format
    username: str

# Valid
u = User(email="test@example.com", username="john")

# Invalid - bad email format
try:
    u = User(email="not-an-email", username="john")
except Exception as e:
    print(e)  # "invalid email format"
```

---

## Dependency Injection

Dependency Injection (DI) is a way to provide resources to functions.

### 1. Basic Dependency

```python
from fastapi import Depends

# Define a dependency
def get_current_user():
    return {"id": 1, "name": "John"}

# Use in endpoint
@app.get("/users/me")
def get_me(user = Depends(get_current_user)):
    return user

# GET /users/me returns:
# {"id": 1, "name": "John"}
```

**Why use DI?**
- Reuse code across multiple endpoints
- Easy testing (swap real DB with fake)
- Automatic documentation

### 2. Database Dependency

```python
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide db to endpoint
    finally:
        db.close()  # Cleanup after endpoint finishes

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    return db_product
```

**How it works:**
1. EndpointNeeds `db` parameter
2. FastAPI calls `get_db()` function
3. `get_db()` opens database connection
4. Returns database to endpoint
5. Endpoint uses it
6. Finally block closes database

### 3. Nested Dependencies

```python
def get_current_user(token: str):
    return {"id": 1, "email": "user@example.com"}

def get_current_admin(user = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(403, "Not authorized")
    return user

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    admin = Depends(get_current_admin)  # Uses get_current_admin
):
    # Only admins can delete
    return {"deleted": product_id}
```

---

## Error Handling

### 1. HTTPException

```python
from fastapi import HTTPException

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id < 1:
        raise HTTPException(
            status_code=400,
            detail="Product ID must be > 0"
        )
    
    if product_id > 1000:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    return {"id": product_id}
```

**Response when error occurs:**
```json
{
    "detail": "Product not found"
}
```

### 2. Custom Error Responses

```python
from fastapi import HTTPException

@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found",
            headers={"X-Error-Code": "PRODUCT_NOT_FOUND"}
        )
    
    return product
```

### 3. Exception Handlers

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

# All HTTPExceptions now return custom format
```

---

## Authentication

Authentication = Verifying who the user is

### 1. Password Hashing

**Never store plain passwords!** Use bcrypt:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

# Hash a password
hashed = pwd_context.hash("mypassword")
# Returns: $2b$12$... (encrypted string)

# Verify a password
is_correct = pwd_context.verify("mypassword", hashed)
# Returns: True
```

### 2. JWT Tokens

JWT = Safe way to identification without storing session

```python
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Create token
def create_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Verify token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None
```

**Token structure:** `Header.Payload.Signature`
- Header: Algorithm info
- Payload: User data
- Signature: Encrypted verification

### 3. Login Endpoint

```python
@app.post("/login")
def login(email: str, password: str):
    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(401, "Invalid credentials")
    
    # Verify password
    if not pwd_context.verify(password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    
    # Create token
    token = create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
```

### 4. Protected Endpoints

```python
from fastapi import Header

async def get_current_user(authorization: str = Header()):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid token")
    
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token")
    
    return payload

@app.get("/users/me")
def get_me(current_user = Depends(get_current_user)):
    return current_user
```

**Usage:**
```
GET /users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Database Integration

### 1. SQLAlchemy Setup

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create engine
engine = create_engine("sqlite:///./test.db")

# Create session factory
SessionLocal = sessionmaker(bind=engine)

# Create base for models
Base = declarative_base()
```

### 2. Define Models

```python
from sqlalchemy import Column, Integer, String

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
```

### 3. Create Tables

```python
Base.metadata.create_all(bind=engine)
```

### 4. CRUD Operations

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

def get_all_products(db: Session):
    return db.query(Product).all()

# UPDATE
def update_product(db: Session, product_id: int, updates):
    product = db.query(Product).filter(Product.id == product_id).first()
    for field, value in updates.dict().items():
        setattr(product, field, value)
    db.commit()
    return product

# DELETE
def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(product)
    db.commit()
```

### 5. Use in Endpoints

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Not found")
    return product
```

---

## Code Organization

### 1. File Structure

```
project/
├── main.py           # Main app file
├── database.py       # Database config
├── models.py         # SQLAlchemy models
├── schemas.py        # Pydantic schemas
├── crud.py           # Database operations
├── auth.py           # Authentication
├── routes/
│   ├── __init__.py
│   ├── products.py
│   ├── users.py
│   └── orders.py
└── requirements.txt
```

### 2. Modular Routers

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
# Endpoints: GET /api/v1/products, POST /api/v1/products
```

---

## Advanced Topics

### 1. Middleware

Middleware runs on every request:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

### 2. Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str):
    # Long-running task
    pass

@app.post("/notify")
def notify(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email)
    return {"message": "Notification queued"}
```

### 3. Events

```python
@app.on_event("startup")
async def startup():
    print("App starting...")

@app.on_event("shutdown")
async def shutdown():
    print("App shutting down...")
```

### 4. Custom Documentation

```python
app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)
```

---

## Summary

You now understand:

✅ HTTP basics (GET, POST, PUT, DELETE)
✅ Path parameters & query parameters
✅ Request bodies & response models
✅ Pydantic validation
✅ Dependency injection
✅ Error handling
✅ Authentication & JWT
✅ Database integration with SQLAlchemy
✅ Project organization
✅ Advanced concepts

Next steps:
1. Build a real project
2. Read FastAPI documentation
3. Contribute to open source
4. Master advanced patterns

**Happy coding!** 🚀
