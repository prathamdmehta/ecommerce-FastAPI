# ============================================
# FastAPI ECOMMERCE APPLICATION - MAIN FILE
# ============================================
# This is the entry point of the FastAPI application
# It initializes the app, includes all routers, and sets up middleware

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Product, Category, User, Order, OrderItem
from routes import products, categories, orders
from schemas import Token, LoginRequest, User as UserSchema, UserCreate
import crud
from auth import hash_password, create_access_token, verify_password
from sqlalchemy.orm import Session

# ===== INITIALIZE DATABASE =====
# This creates all tables defined in models.py
# Run this once when starting the application
Base.metadata.create_all(bind=engine)

# ===== CREATE FASTAPI APP =====
# This is the main FastAPI application instance
app = FastAPI(
    title="Ecommerce API",
    description="A complete ecommerce API with products, categories, orders, and authentication",
    version="1.0.0",
    docs_url="/api/docs",  # Swagger UI documentation at /api/docs
    redoc_url="/api/redoc"  # ReDoc documentation at /api/redoc
)

# ===== CORS CONFIGURATION =====
# CORS (Cross-Origin Resource Sharing) allows requests from different domains
# Useful when your frontend is on a different domain/port than your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (in production, specify exact domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# ===== INCLUDE ROUTERS =====
# Include all API routers with a prefix
# This organizes the API endpoints under /api/v1/
app.include_router(
    products.router,
    prefix="/api/v1",
)

app.include_router(
    categories.router,
    prefix="/api/v1",
)

app.include_router(
    orders.router,
    prefix="/api/v1",
)

# ===== ROOT ENDPOINT =====
@app.get("/", tags=["Health"])
def root():
    """
    Root endpoint - check if API is running.
    
    **Response:**
    ```json
    {
        "message": "Ecommerce API is running!",
        "version": "1.0.0",
        "docs": "/api/docs"
    }
    ```
    """
    return {
        "message": "Ecommerce API is running!",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

# ===== HEALTH CHECK ENDPOINT =====
@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    **Response:**
    ```json
    {
        "status": "healthy"
    }
    ```
    """
    return {"status": "healthy"}

# ===== AUTHENTICATION ENDPOINTS =====

@app.post("/api/v1/auth/register", response_model=UserSchema, tags=["Authentication"], status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "username": "john_doe",
        "password": "secure_password_123"
    }
    ```
    
    **How it works:**
    1. Validates email and username are unique
    2. Hashes the password securely
    3. Creates user in database
    4. Returns user info (without password)
    
    **Valid Passwords:**
    - Minimum 6 characters
    - Maximum 100 characters
    
    **Error Responses:**
    - 400: Email or username already exists
    
    **Response:** Returns created user info
    """
    
    # Check if email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Check if username already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )
    
    # Create new user with hashed password
    db_user = User(
        email=user.email,
        username=user.username,
        password_hash=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/v1/auth/login", response_model=Token, tags=["Authentication"])
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with email and password.
    
    **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "password": "secure_password_123"
    }
    ```
    
    **How it works:**
    1. Finds user by email
    2. Verifies password hash
    3. Creates JWT access token
    4. Returns token
    
    **Token Usage:**
    Include the token in the Authorization header for protected endpoints:
    ```
    Authorization: Bearer <access_token>
    ```
    
    **Token Expiration:**
    Tokens expire after 30 minutes
    
    **Error Responses:**
    - 401: Invalid email or password
    
    **Response:**
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "user": {
            "id": 1,
            "email": "user@example.com",
            "username": "john_doe",
            ...
        }
    }
    ```
    """
    
    # Find user by email
    db_user = db.query(User).filter(User.email == credentials.email).first()
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, db_user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token(user_id=db_user.id, email=db_user.email)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }

# ===== ERROR HANDLERS =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom error handler for HTTP exceptions"""
    return {
        "success": False,
        "message": "An error occurred",
        "detail": exc.detail,
        "status_code": exc.status_code
    }

# ===== STARTUP EVENT =====

@app.on_event("startup")
async def startup_event():
    """
    This function runs when the application starts.
    Useful for initialization tasks like:
    - Loading configuration
    - Initializing databases
    - Setting up connections
    
    In this case, we just print a message.
    """
    print("✅ Ecommerce API is starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """
    This function runs when the application shuts down.
    Useful for cleanup tasks like:
    - Closing database connections
    - Saving state
    - Releasing resources
    """
    print("📛 Ecommerce API is shutting down...")

if __name__ == "__main__":
    """
    This allows running the app directly:
    python main.py
    
    In production, you'd use: uvicorn main:app --host 0.0.0.0 --port 8000
    
    For development with auto-reload: uvicorn main:app --reload
    """
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
