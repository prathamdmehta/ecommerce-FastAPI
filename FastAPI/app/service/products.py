# Import necessary libraries
import json  # For reading/parsing JSON files
from pathlib import Path  # For handling file paths in a cross-platform way
from typing import List, Dict  # For type hints (List of dictionaries)

# Set the path to the products.json file
# Path(__file__) = current file location (products.py)
# .parent.parent = go up TWO folders (service -> app -> FastAPI)
# Then navigate into 'data' folder and find 'products.json'
DATA_FILE = Path(__file__).parent.parent / 'data' / 'products.json'

# FUNCTION 1: Load products from JSON file
def load_prodcuts() -> List[Dict]:
    """Load product data from the JSON file.
    Returns a list of product dictionaries, or an empty list if file doesn't exist.
    """
    # Check if the JSON file exists, if not return empty list
    if not DATA_FILE.exists():
        return []
    
    # Open the file in read mode with UTF-8 encoding
    # 'with' ensures the file is automatically closed after reading
    with open (DATA_FILE, 'r', encoding='utf-8') as file:
        # Parse the JSON file into a Python dictionary
        data = json.load(file)
        # Extract only the "products" array from the JSON
        # The second argument [] is the default value if "products" key doesn't exist
        return data.get("products", [])
    
# FUNCTION 2: Public function to get all products
def get_all_products() -> List[Dict]:
    """Wrapper function that calls load_prodcuts() to get all products."""
    return load_prodcuts()