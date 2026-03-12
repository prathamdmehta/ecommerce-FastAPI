# ============================================
# ORDERS API ENDPOINTS
# ============================================
# Handle order creation, retrieval, and management

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import Order, OrderCreate, OrderDetail, OrderUpdate
import crud

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={404: {"description": "Not found"}}
)

# ===== CREATE ORDER =====
@router.post("/", response_model=Order, status_code=201, summary="Create new order")
def create_order(
    user_id: int,
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new order with one or more items.
    
    **Query Parameters:**
    - `user_id`: ID of the user placing the order
    
    **Request Body:**
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
    
    **How it works:**
    1. Validates all products exist
    2. Checks stock availability
    3. Calculates total price
    4. Creates order and order items
    5. Reduces product stock
    
    **Error Responses:**
    - 404: Product not found
    - 400: Insufficient stock or other validation error
    
    **Response:** Returns the created order with all items
    """
    try:
        db_order = crud.create_order(db, user_id, order)
        return db_order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ===== GET ORDER BY ID =====
@router.get("/{order_id}", response_model=OrderDetail, summary="Get order by ID")
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Get a specific order with all its items and user information.
    
    **Path Parameters:**
    - `order_id`: The ID of the order
    
    **Response:**
    ```json
    {
        "id": 1,
        "user_id": 1,
        "total_price": 299.98,
        "status": "pending",
        "created_at": "2024-01-20T10:30:00",
        "items": [
            {
                "id": 1,
                "product_id": 1,
                "quantity": 2,
                "price": 99.99,
                "product": {...}
            }
        ],
        "user": {...}
    }
    ```
    
    **Error Responses:**
    - 404: Order not found
    """
    db_order = crud.get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(
            status_code=404,
            detail=f"Order with ID {order_id} not found"
        )
    return db_order

# ===== GET USER'S ORDERS =====
@router.get("/user/{user_id}", response_model=list[Order], summary="Get user's orders")
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    """
    Get all orders placed by a specific user.
    
    **Path Parameters:**
    - `user_id`: The ID of the user
    
    **Response:**
    ```json
    [
        {
            "id": 1,
            "user_id": 1,
            "total_price": 299.98,
            "status": "pending",
            "created_at": "2024-01-20T10:30:00",
            "items": [...]
        }
    ]
    ```
    """
    orders = crud.get_user_orders(db, user_id)
    return orders

# ===== UPDATE ORDER STATUS =====
@router.put("/{order_id}/status", response_model=Order, summary="Update order status")
def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db)
):
    """
    Update the status of an order.
    
    **Path Parameters:**
    - `order_id`: ID of the order to update
    
    **Request Body:**
    ```json
    {
        "status": "completed"
    }
    ```
    
    **Allowed Statuses:**
    - `pending`: Order received but not processed
    - `processing`: Order is being prepared
    - `shipped`: Order is on the way
    - `completed`: Order delivered
    - `cancelled`: Order cancelled
    
    **Error Responses:**
    - 404: Order not found
    """
    db_order = crud.update_order_status(db, order_id, order_update.status)
    if not db_order:
        raise HTTPException(
            status_code=404,
            detail=f"Order with ID {order_id} not found"
        )
    return db_order

# ===== CANCEL ORDER =====
@router.post("/{order_id}/cancel", response_model=Order, summary="Cancel order")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    """
    Cancel an order and restore product stock.
    
    **Path Parameters:**
    - `order_id`: ID of the order to cancel
    
    **How it works:**
    1. Checks if order is cancellable (not completed)
    2. Restores stock for all items in the order
    3. Updates order status to "cancelled"
    
    **Important:**
    - Cannot cancel orders that are already completed
    - Stock is immediately restored
    
    **Error Responses:**
    - 404: Order not found
    - 400: Cannot cancel (order already completed)
    """
    try:
        db_order = crud.cancel_order(db, order_id)
        if not db_order:
            raise HTTPException(
                status_code=404,
                detail=f"Order with ID {order_id} not found"
            )
        return db_order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
