# ============================================
# AUTHENTICATION UTILITIES
# ============================================
# Functions for password hashing and JWT token management
# Security is critical in web applications!

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# ===== PASSWORD HASHING =====

# Create a password context using bcrypt algorithm
# bcrypt is one of the most secure password hashing algorithms
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Why hash passwords?
    - Never store plain passwords in the database
    - If database is leaked, passwords are still secure
    - Hashing is one-way: you can verify a password by hashing it and comparing
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash.
    
    Args:
        plain_password: Password provided by user
        hashed_password: Hashed password from database
    
    Returns:
        True if passwords match, False otherwise
    
    Example:
        Plain password: "mypassword123"
        Hash in DB: "$2b$12$..." (bcrypt hash)
        verify_password("mypassword123", "$2b$12$...") -> True
    """
    return pwd_context.verify(plain_password, hashed_password)

# ===== JWT TOKEN MANAGEMENT =====

# JWT Secret key - in production, load from environment variable
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user_id: int, email: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token for a user.
    
    JWT (JSON Web Token) is a standard way to pass authenticated user info.
    Structure: Header.Payload.Signature
    
    Args:
        user_id: User ID to encode in token
        email: User email to encode in token
        expires_delta: How long token is valid (default: 30 minutes)
    
    Returns:
        JWT token string
    
    Example Token Content:
    {
        "user_id": 123,
        "email": "user@example.com",
        "exp": 1234567890  # Expiration time
    }
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create the token payload (data to encode)
    to_encode = {
        "user_id": user_id,
        "email": email,
        "exp": expire
    }
    
    # Encode and sign the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT access token.
    
    Args:
        token: JWT token to verify
    
    Returns:
        Token payload (dict) if valid, None if invalid or expired
    
    Example:
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        payload = verify_access_token(token)
        # Returns: {"user_id": 123, "email": "user@example.com", "exp": ...}
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Token is invalid or expired
        return None
