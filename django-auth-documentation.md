# Django Authentication System

## Overview

This project provides a complete authentication system built with Django and Django REST Framework, using JWT tokens for secure authentication. The system supports user registration, login, token refresh, and profile management.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [API Documentation](#api-documentation)
6. [Changelog](#changelog)
7. [Development Guide](#development-guide)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Contributing](#contributing)

## Features

- User registration with email and username
- JWT authentication (access and refresh tokens)
- Token refresh mechanism
- User profile management
- Password reset functionality
- Email verification (optional)
- Role-based permissions (optional)
- PostgreSQL database integration
- Swagger API documentation

## Requirements

- Python 3.8+
- PostgreSQL 12+
- Django 5.0+
- Django REST Framework 3.14+
- Django REST Framework SimpleJWT 5.3+

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:
```bash
# Login to PostgreSQL shell
sudo -u postgres psql

# Create database and user
CREATE DATABASE amankan_db;
CREATE USER your_user WITH PASSWORD 'admin';
ALTER ROLE your_user SET client_encoding TO 'utf8';
ALTER ROLE your_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE amankan_db TO your_user;
GRANT ALL ON SCHEMA public TO your_user;
\q
```

5. Create a `.env` file:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=amankan_db
DB_USER=your_user
DB_PASSWORD=admin
DB_HOST=localhost
DB_PORT=5432
```

6. Run migrations:
```bash
python manage.py makemigrations amankan
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

## Configuration

### Swagger Setup

1. Install drf-yasg:
```bash
pip install drf-yasg
```

2. Add to `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'drf_yasg',
    # ...
]
```

3. Configure Swagger in `urls.py`:
```python
from django.urls import path, include, re_path
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Authentication API",
      default_version='v1',
      description="API documentation for Authentication System",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('amankan.api.urls')),
    
    # Swagger documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

### JWT Configuration

Adjust JWT settings in `settings.py`:

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}
```

## API Documentation

### Endpoints

#### Authentication

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/auth/register/` | POST | Register a new user | `{"email": "user@example.com", "username": "user", "password": "password123"}` | `{"id": 1, "email": "user@example.com", "username": "user"}` |
| `/api/auth/login/` | POST | Login and get tokens | `{"email": "user@example.com", "password": "password123"}` | `{"access": "token", "refresh": "token", "user": {...}}` |
| `/api/auth/token/refresh/` | POST | Refresh access token | `{"refresh": "token"}` | `{"access": "new_token", "refresh": "new_refresh_token"}` |
| `/api/auth/profile/` | GET | Get user profile | | `{"id": 1, "email": "user@example.com", "username": "user"}` |
| `/api/auth/profile/` | PUT/PATCH | Update user profile | `{"username": "new_username"}` | `{"id": 1, "email": "user@example.com", "username": "new_username"}` |

#### Optional Endpoints (Future Implementation)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/password/reset/` | POST | Request password reset |
| `/api/auth/password/reset/confirm/` | POST | Confirm password reset |
| `/api/auth/verify-email/` | POST | Verify email address |
| `/api/auth/logout/` | POST | Logout (blacklist token) |

### Authentication

All secured endpoints require the following header:
```
Authorization: Bearer <access_token>
```

### API Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

## Changelog

### Version 1.0.0 (Initial Release)
- Basic user registration and authentication
- JWT token-based authentication
- User profile management
- PostgreSQL integration
- Swagger documentation

### Version 1.1.0 (Planned)
- Password reset functionality
- Email verification
- Token blacklisting for logout
- Enhanced security features

### Version 1.2.0 (Planned)
- Role-based permissions
- User groups and permissions
- Activity logging
- Two-factor authentication

## Development Guide

### Project Structure

```
├── core/                   # Project configuration
│   ├── settings/           
│   │   ├── __init__.py
│   │   └── base.py         # Base settings
│   ├── urls.py             # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
├── amankan/                # Authentication app
│   ├── api/                # API components
│   │   ├── serializers.py  # Data serialization
│   │   ├── urls.py         # API endpoints
│   │   └── views.py        # API logic
│   ├── migrations/
│   ├── models.py           # Database models
│   ├── admin.py            # Admin interface
│   └── tests.py            # Unit tests
├── manage.py
├── requirements.txt
├── .env                    # Environment variables
└── README.md
```

### Coding Standards

- Follow PEP 8 for Python code style
- Use Django's coding style for Django-specific components
- Write docstrings for all functions and classes
- Keep functions small and focused on a single task
- Write unit tests for all functionality

### Environment Setup

We recommend using environment variables for all sensitive information:

```python
# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test amankan.tests.test_api
```

### Test Coverage

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test amankan

# Generate report
coverage report
coverage html  # For HTML report
```

### Sample Test Cases

```python
# amankan/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'password123'
        }

    def test_user_registration(self):
        response = self.client.post(
            self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_user_login(self):
        # Create a user
        User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password123'
        )
        
        # Login
        response = self.client.post(
            self.login_url,
            {
                'email': 'test@example.com',
                'password': 'password123'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
```

## Deployment

### Production Settings

Create a production settings file `core/settings/production.py`:

```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Database - use environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
```

### Deployment Checklist

- Set `DEBUG = False` in production settings
- Configure proper `ALLOWED_HOSTS`
- Use environment variables for sensitive data
- Set up HTTPS with valid SSL certificate
- Collect static files: `python manage.py collectstatic`
- Properly set up database backups
- Configure logging
- Set up monitoring for the application

### Deployment Options

1. **Traditional Server**
   - Gunicorn/uWSGI as application server
   - Nginx as reverse proxy
   - PostgreSQL database
   - Systemd for process management

2. **Docker**
   - Containerize application with Docker
   - Use Docker Compose for local development
   - Deploy to container orchestration (Kubernetes, ECS)

3. **PaaS**
   - Deploy to Heroku, DigitalOcean App Platform, etc.
   - Configure PostgreSQL add-on

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

### Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the CHANGELOG.md with version details
3. Ensure all tests pass
4. Get approval from at least one reviewer before merging
