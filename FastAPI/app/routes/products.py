# ============================================
# PRODUCTS API ENDPOINTS
# ============================================
# All product-related endpoints are organized here

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import Product, ProductCreate, ProductUpdate
import crud

# Create a router for products
# This allows us to organize endpoints by feature
# We'll include this router in the main app with prefix='/api/v1/products'
router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}}
)

# ===== GET ALL PRODUCTS =====
@router.get("/", response_model=dict, summary="Get all products")
def list_products(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum products to return"),
    name: str = Query(None, description="Search by product name"),
    sort_by_price: bool = Query(False, description="Sort by price"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Sort order")
):
    """
    Get all products with optional filtering and sorting.
    
    **Query Parameters:**
    - `skip`: Skip first N products (pagination)
    - `limit`: Number of products to return (max 100)
    - `name`: Filter by product name (case-insensitive)
    - `sort_by_price`: Sort by price (true/false)
    - `order`: Sort order (asc/desc)
    
    **Examples:**
    - `/api/v1/products/` - Get first 10 products
    - `/api/v1/products/?name=keyboard` - Search for "keyboard"
    - `/api/v1/products/?sort_by_price=true&order=desc` - Most expensive first
    
    **Response Format:**
    ```json
    {
        "total": 100,
        "items": [
            {
                "id": 1,
                "name": "Product Name",
                "price": 99.99,
                ...
            }
        ],
        "skip": 0,
        "limit": 10
    }
    ```
    """
    
    # Get products
    products = crud.get_products(db, skip=skip, limit=limit)
    
    # Filter by name if provided
    if name:
        products = [p for p in products if name.lower() in p.name.lower()]
    
    # Sort by price if requested
    if sort_by_price:
        reverse = order == "desc"
        products = sorted(products, key=lambda p: p.price, reverse=reverse)
    
    return {
        "total": len(products),
        "items": products,
        "skip": skip,
        "limit": limit
    }

# ===== GET SINGLE PRODUCT =====
@router.get("/{product_id}", response_model=Product, summary="Get product by ID")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a single product by its ID.
    
    **Path Parameters:**
    - `product_id`: The ID of the product to retrieve
    
    **Example:** `/api/v1/products/5`
    
    **Error Responses:**
    - 404: Product not found
    """
    
    db_product = crud.get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )
    return db_product

# ===== CREATE PRODUCT =====
@router.post("/", response_model=Product, status_code=201, summary="Create new product")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    
    **Request Body:**
    ```json
    {
        "name": "Laptop",
        "description": "High performance laptop",
        "price": 999.99,
        "currency": "USD",
        "color": "Silver",
        "image": "url-to-image",
        "stock": 50,
        "rating": 4.5,
        "category_id": 1
    }
    ```
    
    **Response:** Returns the created product with assigned ID
    
    **Status:** 201 Created
    """
    
    # Check if category exists
    from models import Category
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(
            status_code=400,
            detail=f"Category with ID {product.category_id} not found"
        )
    
    return crud.create_product(db, product)

# ===== UPDATE PRODUCT =====
@router.put("/{product_id}", response_model=Product, summary="Update product")
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing product.
    
    **Path Parameters:**
    - `product_id`: ID of the product to update
    
    **Request Body:** (All fields optional)
    ```json
    {
        "name": "Updated Name",
        "price": 1099.99
    }
    ```
    
    **Note:** Only provide fields you want to update
    
    **Error Responses:**
    - 404: Product not found
    """
    
    db_product = crud.update_product(db, product_id, product_update)
    if not db_product:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )
    return db_product

# ===== DELETE PRODUCT =====
@router.delete("/{product_id}", summary="Delete product")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product permanently.
    
    **Path Parameters:**
    - `product_id`: ID of the product to delete
    
    **Response:**
    ```json
    {
        "message": "Product deleted successfully"
    }
    ```
    
    **Error Responses:**
    - 404: Product not found
    
    **Warning:** This action is permanent and cannot be undone!
    """
    
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )
    
    return {"message": "Product deleted successfully"}
