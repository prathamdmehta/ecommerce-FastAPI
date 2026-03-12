# 🚀 Ecommerce FastAPI Application

A complete, production-ready ecommerce API built with FastAPI, SQLAlchemy, and Pydantic.

## ✨ Features

- **User Authentication** - JWT-based secure authentication
- **Product Management** - Full CRUD operations for products
- **Category System** - Organize products into categories
- **Order Processing** - Complete order management with stock control
- **API Documentation** - Auto-generated Swagger UI & ReDoc
- **Data Validation** - Automatic request/response validation
- **Database** - SQLite with SQLAlchemy ORM
- **Error Handling** - Comprehensive error responses
- **Code Organization** - Clean, modular structure

---

## 📋 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment

```bash
cd FastAPI/app
cp .env.example .env
```

Update `.env` with your settings if needed.

### 3. Initialize Database

```bash
python init_db.py
```

This creates the database tables and populates with sample data.

### 4. Run the Server

```bash
uvicorn main_new:app --reload
```

Output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 5. Access the Application

- **API Documentation**: http://localhost:8000/api/docs
- **Alternative Docs**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

---

## 📚 Documentation

### API Reference
**File**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

Complete API endpoint reference with:
- All available endpoints
- Request/response examples
- Query parameters
- Error responses

### FastAPI Learning Guide
**File**: [FASTAPI_LEARNING_GUIDE.md](FASTAPI_LEARNING_GUIDE.md)

Comprehensive FastAPI tutorial covering:
- Basic concepts
- Request/response handling
- Data validation
- Authentication
- Database integration
- Best practices

---

## 🔐 Test Credentials

After running `init_db.py`, use these credentials:

```
Email: demo@example.com
Username: demouser
Password: password123
```

Or:

```
Email: john@example.com
Username: john_doe
Password: securepass456
```

---

## 📁 Project Structure

```
FastAPI/
├── app/
│   ├── main_new.py              ← START HERE (refactored app)
│   ├── main.py                  (original, kept for reference)
│   ├── database.py              (database configuration)
│   ├── models.py                (SQLAlchemy ORM models)
│   ├── schemas.py               (Pydantic validation schemas)
│   ├── crud.py                  (database operations)
│   ├── auth.py                  (authentication utilities)
│   ├── init_db.py               (database initialization)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── products.py          (product endpoints)
│   │   ├── categories.py        (category endpoints)
│   │   └── orders.py            (order endpoints)
│   ├── service/                 (original service layer)
│   ├── data/                    (original data files)
│   ├── ecommerce.db             (SQLite database - auto-created)
│   ├── API_DOCUMENTATION.md     ← READ THIS
│   ├── FASTAPI_LEARNING_GUIDE.md ← LEARN FROM THIS
│   └── .env.example             (environment template)
└── requirements.txt
```

---

## 🎯 Key Concepts

### Models
Python classes that represent database tables. Defined in `models.py`.

### Schemas
Pydantic classes for data validation and API documentation. Defined in `schemas.py`.

### CRUD Operations
Create, Read, Update, Delete functions for database operations. Defined in `crud.py`.

### Routes
API endpoints organized by feature (products, categories, orders). Found in `routes/` directory.

### Authentication
JWT-based authentication for secure API access. Utilities in `auth.py`.

---

## 🔗 API Endpoints Overview

### Authentication
```
POST   /api/v1/auth/register     - Create new user
POST   /api/v1/auth/login        - Login and get token
```

### Products
```
GET    /api/v1/products          - Get all products (with filtering/sorting)
GET    /api/v1/products/{id}     - Get specific product
POST   /api/v1/products          - Create product
PUT    /api/v1/products/{id}     - Update product
DELETE /api/v1/products/{id}     - Delete product
```

### Categories
```
GET    /api/v1/categories        - Get all categories
GET    /api/v1/categories/{id}   - Get specific category
POST   /api/v1/categories        - Create category
PUT    /api/v1/categories/{id}   - Update category
DELETE /api/v1/categories/{id}   - Delete category
```

### Orders
```
POST   /api/v1/orders            - Create order
GET    /api/v1/orders/{id}       - Get order details
GET    /api/v1/orders/user/{id}  - Get user's orders
PUT    /api/v1/orders/{id}/status - Update order status
POST   /api/v1/orders/{id}/cancel - Cancel order
```

---

## 🧪 Testing

### Using Swagger UI (Easiest)

1. Open http://localhost:8000/api/docs
2. Click endpoint to expand it
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. See response

### Using curl

#### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "username": "newuser",
    "password": "password123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "password123"
  }'
```

Response includes token:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {...}
}
```

#### Get Products
```bash
curl http://localhost:8000/api/v1/products
curl http://localhost:8000/api/v1/products?sort_by_price=true&order=desc
curl "http://localhost:8000/api/v1/products?name=laptop"
```

---

## 📚 Learning Path

1. **Read API_DOCUMENTATION.md** - Understand endpoints
2. **Read FASTAPI_LEARNING_GUIDE.md** - Learn FastAPI concepts
3. **Explore main_new.py** - See how it's organized
4. **Test with Swagger UI** - Try endpoints
5. **Modify the code** - Add your own features

---

## 🔧 Common Commands

### Start Development Server
```bash
cd FastAPI/app
uvicorn main_new:app --reload
```

### Run with Different Port
```bash
uvicorn main_new:app --port 8001
```

### Initialize Fresh Database
```bash
rm ecommerce.db  # Delete old database
python init_db.py  # Create new
```

### Check Python Version
```bash
python --version
```

### Install New Packages
```bash
pip install package_name
pip freeze > requirements.txt  # Update requirements
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Address already in use"
**Solution**: Use a different port
```bash
uvicorn main_new:app --port 8001
```

### Issue: Database errors
**Solution**: Reinitialize database
```bash
rm ecommerce.db
python init_db.py
```

### Issue: Import errors
**Solution**: Ensure you're in the correct directory
```bash
cd FastAPI/app
python -c "import main_new"  # Should not error
```

---

## 📖 Additional Resources

- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [JWT Explanation](https://jwt.io/)

---

## 🎓 What You'll Learn

By exploring this project, you'll understand:

- **REST API Design** - How to build scalable APIs
- **FastAPI Framework** - Modern Python web framework
- **Database Design** - Relationships and CRUD operations
- **Authentication** - JWT tokens and password hashing
- **Code Organization** - Professional project structure
- **Error Handling** - Proper HTTP status codes
- **API Documentation** - Auto-generation and examples

---

## 🚀 Next Steps

1. **Extend Features**
   - Add reviews/ratings
   - Implement cart functionality
   - Add payment processing

2. **Improve Database**
   - Add PostgreSQL support
   - Implement migrations
   - Add indexing

3. **Deployment**
   - Deploy to AWS/Heroku/DigitalOcean
   - Setup CI/CD pipeline
   - Add monitoring

4. **Testing**
   - Write unit tests
   - Add integration tests
   - Setup pytest

---

## 📝 Files to Read First

1. **API_DOCUMENTATION.md** - Complete API reference
2. **FASTAPI_LEARNING_GUIDE.md** - FastAPI concepts
3. **main_new.py** - Application entry point
4. **models.py** - Database structure
5. **routes/products.py** - Example of endpoint organization

---

## 💡 Tips

- **Use Swagger UI** - It's your best friend for testing
- **Read comments** - Every file has detailed comments
- **Start small** - Understand one endpoint before exploring others
- **Experiment** - Modify code and see what happens
- **Use tools** - Postman, curl, or Thunder Client for API testing

---

## 📄 License

This project is educational. Use freely!

---

## ❓ Questions?

If you have questions:
1. Check the learning guide - **FASTAPI_LEARNING_GUIDE.md**
2. Review API documentation - **API_DOCUMENTATION.md**
3. Look at code comments
4. Try concepts in Swagger UI

---

**Happy learning! Build amazing APIs with FastAPI! 🎉**
