# ============================================
# CATEGORIES API ENDPOINTS
# ============================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import Category, CategoryCreate, CategoryUpdate
import crud

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    responses={404: {"description": "Not found"}}
)

# ===== GET ALL CATEGORIES =====
@router.get("/", response_model=list[Category], summary="Get all categories")
def list_categories(db: Session = Depends(get_db)):
    """
    Get all product categories.
    
    **Response:**
    ```json
    [
        {
            "id": 1,
            "name": "Electronics",
            "description": "Electronic devices",
            "image": "url"
        }
    ]
    ```
    """
    return crud.get_categories(db)

# ===== GET SINGLE CATEGORY =====
@router.get("/{category_id}", response_model=Category, summary="Get category by ID")
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get a single category with all its products.
    
    **Path Parameters:**
    - `category_id`: The ID of the category
    
    **Error Responses:**
    - 404: Category not found
    """
    db_category = crud.get_category_by_id(db, category_id)
    if not db_category:
        raise HTTPException(
            status_code=404,
            detail=f"Category with ID {category_id} not found"
        )
    return db_category

# ===== CREATE CATEGORY =====
@router.post("/", response_model=Category, status_code=201, summary="Create new category")
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new product category.
    
    **Request Body:**
    ```json
    {
        "name": "Laptops",
        "description": "Portable computers",
        "image": "url-to-image"
    }
    ```
    
    **Response:** Returns the created category with assigned ID
    """
    return crud.create_category(db, category)

# ===== UPDATE CATEGORY =====
@router.put("/{category_id}", response_model=Category, summary="Update category")
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing category.
    
    **Path Parameters:**
    - `category_id`: ID of the category to update
    
    **Request Body:** (All fields optional)
    
    **Error Responses:**
    - 404: Category not found
    """
    db_category = crud.update_category(db, category_id, category_update)
    if not db_category:
        raise HTTPException(
            status_code=404,
            detail=f"Category with ID {category_id} not found"
        )
    return db_category

# ===== DELETE CATEGORY =====
@router.delete("/{category_id}", summary="Delete category")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category permanently.
    
    **Warning:** This will not delete products in this category, but they'll be orphaned!
    
    **Error Responses:**
    - 404: Category not found
    """
    deleted = crud.delete_category(db, category_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Category with ID {category_id} not found"
        )
    return {"message": "Category deleted successfully"}
