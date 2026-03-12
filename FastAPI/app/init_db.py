# ============================================
# DATABASE INITIALIZATION SCRIPT
# ============================================
# Run this once to populate the database with sample data
# python init_db.py

from database import SessionLocal, engine, Base
from models import Category, Product, User
from auth import hash_password
from datetime import datetime

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Check if data already exists
    existing_categories = db.query(Category).count()
    if existing_categories > 0:
        print("Database already has data. Skipping initialization.")
        exit()
    
    print("🗄️  Creating database tables...")
    
    # ===== CREATE CATEGORIES =====
    print("📦 Creating categories...")
    
    categories = [
        Category(
            name="Electronics",
            description="Electronic devices and gadgets",
            image="https://images.unsplash.com/photo-1550355291-bbee04a92027?w=400"
        ),
        Category(
            name="Books",
            description="Physical books and reading materials",
            image="https://images.unsplash.com/photo-1507842217343-583f20270319?w=400"
        ),
        Category(
            name="Clothing",
            description="Apparel and fashion items",
            image="https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=400"
        ),
        Category(
            name="Home & Garden",
            description="Home improvement and garden products",
            image="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400"
        ),
        Category(
            name="Sports & Outdoors",
            description="Sports equipment and outdoor gear",
            image="https://images.unsplash.com/photo-1517836357463-d25ddfcbf042?w=400"
        )
    ]
    
    db.add_all(categories)
    db.commit()
    
    print(f"✅ Created {len(categories)} categories")
    
    # ===== CREATE PRODUCTS =====
    print("📱 Creating products...")
    
    products = [
        # Electronics
        Product(
            name="Laptop Pro",
            description="High-performance laptop with 16GB RAM and 512GB SSD",
            price=1299.99,
            currency="USD",
            color="Silver",
            image="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400",
            stock=15,
            rating=4.8,
            category_id=1
        ),
        Product(
            name="Wireless Headphones",
            description="Noise-cancelling Bluetooth headphones with 30 hour battery",
            price=199.99,
            currency="USD",
            color="Black",
            image="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
            stock=50,
            rating=4.5,
            category_id=1
        ),
        Product(
            name="USB-C Hub",
            description="7-in-1 USB-C hub with HDMI and SD card reader",
            price=49.99,
            currency="USD",
            color="Space Gray",
            image="https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400",
            stock=100,
            rating=4.2,
            category_id=1
        ),
        
        # Books
        Product(
            name="Python Programming",
            description="Complete guide to Python programming for beginners",
            price=39.99,
            currency="USD",
            color="Multi-color",
            image="https://images.unsplash.com/photo-1507842217343-583f20270319?w=400",
            stock=30,
            rating=4.7,
            category_id=2
        ),
        Product(
            name="Web Development Essentials",
            description="Learn web development with HTML, CSS, and JavaScript",
            price=44.99,
            currency="USD",
            color="Multi-color",
            image="https://images.unsplash.com/photo-1507842217343-583f20270319?w=400",
            stock=25,
            rating=4.4,
            category_id=2
        ),
        
        # Clothing
        Product(
            name="Cotton T-Shirt",
            description="100% organic cotton comfort t-shirt",
            price=29.99,
            currency="USD",
            color="Blue",
            image="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
            stock=200,
            rating=4.3,
            category_id=3
        ),
        Product(
            name="Denim Jeans",
            description="Classic blue denim jeans with comfort fit",
            price=69.99,
            currency="USD",
            color="Dark Blue",
            image="https://images.unsplash.com/photo-1542272604-787c62d465d1?w=400",
            stock=80,
            rating=4.6,
            category_id=3
        ),
        
        # Home & Garden
        Product(
            name="Smart Light Bulb",
            description="WiFi-enabled LED light bulb with color control",
            price=24.99,
            currency="USD",
            color="White",
            image="https://images.unsplash.com/photo-1565636192335-14c46fa1120d?w=400",
            stock=150,
            rating=4.5,
            category_id=4
        ),
        Product(
            name="Coffee Maker",
            description="Programmable coffee maker with thermal carafe",
            price=89.99,
            currency="USD",
            color="Black",
            image="https://images.unsplash.com/photo-1517668808822-9ebb02ae2a0e?w=400",
            stock=40,
            rating=4.4,
            category_id=4
        ),
        
        # Sports & Outdoors
        Product(
            name="Yoga Mat",
            description="Non-slip exercise yoga mat with carrying strap",
            price=34.99,
            currency="USD",
            color="Purple",
            image="https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400",
            stock=120,
            rating=4.7,
            category_id=5
        ),
        Product(
            name="Running Shoes",
            description="Professional running shoes with gel cushioning",
            price=129.99,
            currency="USD",
            color="Black & Red",
            image="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
            stock=60,
            rating=4.6,
            category_id=5
        ),
    ]
    
    db.add_all(products)
    db.commit()
    
    print(f"✅ Created {len(products)} products")
    
    # ===== CREATE SAMPLE USERS =====
    print("👥 Creating sample users...")
    
    users = [
        User(
            email="demo@example.com",
            username="demouser",
            password_hash=hash_password("password123"),
            is_active=True
        ),
        User(
            email="john@example.com",
            username="john_doe",
            password_hash=hash_password("securepass456"),
            is_active=True
        ),
        User(
            email="jane@example.com",
            username="jane_smith",
            password_hash=hash_password("mypassword789"),
            is_active=True
        ),
    ]
    
    db.add_all(users)
    db.commit()
    
    print(f"✅ Created {len(users)} users")
    
    print("\n" + "="*50)
    print("✅ Database initialization completed!")
    print("="*50)
    print("\n📝 Sample Credentials for Testing:")
    print("-" * 50)
    print("Email: demo@example.com")
    print("Username: demouser")
    print("Password: password123")
    print("-" * 50)
    print("\nEmail: john@example.com")
    print("Username: john_doe")
    print("Password: securepass456")
    print("-" * 50)
    print("\n🚀 Ready to use! Run: uvicorn main_new:app --reload")
    print("📚 API Docs available at: http://localhost:8000/api/docs")
    
except Exception as e:
    print(f"❌ Error during initialization: {e}")
    db.rollback()
finally:
    db.close()
