# Django Authentication API System

A secure, scalable authentication system built with Django REST Framework and JWT.

## Features

✅ User registration with email and username  
✅ JWT authentication with access and refresh tokens  
✅ User profile management  
✅ PostgreSQL database integration  
✅ Swagger API documentation  
✅ Token refresh mechanism  

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```

2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure PostgreSQL
```bash
# In PostgreSQL shell
CREATE DATABASE amankan_db;
CREATE USER your_user WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE amankan_db TO your_user;
```

5. Create `.env` file
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=amankan_db
DB_USER=your_user
DB_PASSWORD=admin
DB_HOST=localhost
DB_PORT=5432
```

6. Run migrations
```bash
python manage.py makemigrations amankan
python manage.py migrate
```

7. Create superuser
```bash
python manage.py createsuperuser
```

8. Run the server
```bash
python manage.py runserver
```

## API Documentation

Access the API documentation at:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

### Main Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | Register a new user |
| `/api/auth/login/` | POST | Login and get tokens |
| `/api/auth/token/refresh/` | POST | Refresh access token |
| `/api/auth/profile/` | GET | Get user profile |
| `/api/auth/profile/` | PUT | Update user profile |

## Development

For detailed development instructions, please refer to the [Development Guide](docs/development.md).

## Testing

Run tests with:
```bash
python manage.py test
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
