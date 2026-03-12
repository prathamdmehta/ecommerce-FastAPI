# Import FastAPI components
from fastapi import FastAPI, HTTPException, Query
# Import the function to get products from the service layer
from service.products import get_all_products

# Create a FastAPI application instance
app = FastAPI()

# ===== ENDPOINT 1: ROOT ENDPOINT =====
@app.get('/')  # This creates a GET route at http://localhost:8000/
def root():
    """Simple welcome message endpoint."""
    return {'message': 'Hellow World'}

# ===== ENDPOINT 2: LIST PRODUCTS ENDPOINT =====
@app.get('/products')  # This creates a GET route at http://localhost:8000/products
def list_products(name: str = Query(
    default=None,  # Query parameter is optional (default is None)
    min_length=1,  # If provided, name must be at least 1 character
    max_length=50,  # If provided, name must not exceed 50 characters
    description="Search Product by Name (case insensitive)", # Help text for API documentation
), 
    sort_by_price: bool= Query(default=False, description="Sorts products by price"),
    order: str= Query(default='asc', description='Sort products in asc,desc')
):
    """Get a list of all products, optionally filtered by name and sorted by price.
    
    Args:
        name: Optional query parameter to search products by name
              Example: /products?name=keyboard
        sort_by_price: Optional boolean to enable sorting by price (default: False)
                      Example: /products?sort_by_price=true
        order: Sort order when sort_by_price is enabled - 'asc' or 'desc' (default: 'asc')
               Example: /products?sort_by_price=true&order=desc
    
    Returns:
        A dictionary with 'total' (count) and 'items' (list of products)
    """
    
    # STEP 1: Fetch all products from the JSON file
    products = get_all_products()
    
    # STEP 2: Count total products (will be updated if filtering is applied)
    total = len(products)  # Initially set to all products count
    
    # STEP 3: If user provided a name search parameter, filter the results
    if name:
        # Convert search term to lowercase and remove extra spaces
        needle = name.strip().lower()
        
        # Filter products: keep only those whose name contains the search term
        # This happens case-insensitive because both sides are converted to lowercase
        products = [p for p in products if needle in p.get("name", "").lower()]
        
        # STEP 4: If no products match the search, raise a 404 error
        if not products:
            raise HTTPException(
                status_code=404, 
                detail=f"No product found matching name={name}"
            )
        
    # STEP 4: If user requested sorting by price, sort the products
    if sort_by_price:
        # Determine the sort order: reverse=True for descending, reverse=False for ascending
        # This compares the order parameter with 'desc' string
        reverse = order == "desc"
        
        # Sort the products list by the 'price' field using sorted() function
        # lambda p: p.get('price', 0) extracts the price from each product
        # If price doesn't exist, it defaults to 0
        # reverse=True sorts in descending order (highest to lowest)
        # reverse=False sorts in ascending order (lowest to highest)
        products = sorted(products, key=lambda p: p.get('price', 0), reverse=reverse)
        
    # STEP 5: Update total count to reflect filtered/sorted results
    total = len(products)
    
    # STEP 6: Return the results as JSON
    return {
        "total": total,  # Number of products found
        "items": products  # List of product dictionaries
    }