# Drink Recipe Finder

![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Django](https://img.shields.io/badge/Django-4.0+-darkgreen)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A production-grade, containerized web application that bridges real-time cocktail data from TheCocktailDB API with local persistence, enabling users to discover drinks, save favorites, and share reviews.

## 🎯 Overview

Drink Recipe Finder demonstrates a **Hybrid Data Architecture** that seamlessly merges external API data with local user persistence. The application features a fully automated CI/CD pipeline, containerized deployment, and comprehensive test coverage—showcasing DevOps best practices for modern web applications.

**Key Highlights:**
- Real-time cocktail data from TheCocktailDB with lazy-loaded local persistence
- Full social engine: user favorites, ratings, and reviews
- Automated CI/CD pipeline with zero-downtime deployment
- Production-ready Docker setup with Nginx and Gunicorn
- Comprehensive test suite with mocked external dependencies

## 🏗️ Architecture

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Django 4.0+ | Application framework |
| **Server** | Gunicorn | WSGI application server |
| **Web Server** | Nginx | Reverse proxy & static files |
| **Database** | PostgreSQL 15 | Persistent storage |
| **External API** | TheCocktailDB | Recipe data source |
| **Testing** | Pytest + Mock | Automated quality assurance |
| **Frontend** | Bootstrap 5 | Responsive UI framework |

### System Design

```
┌─────────────────────────────────────────┐
│         User Browser (Frontend)         │
│      Bootstrap 5 + Django Templates     │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│       Nginx (Reverse Proxy)             │
│    Static Files & Load Balancing        │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│   Django + Gunicorn (App Server)        │
│   • Search & Browse Recipes             │
│   • User Authentication                 │
│   • Favorites Management                │
│   • Review System                       │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐  ┌────────▼────────┐
│  PostgreSQL    │  │ TheCocktailDB   │
│  (Local DB)    │  │  (External API) │
│                │  │                 │
│ • Users        │  │ • Recipes       │
│ • Favorites    │  │ • Ingredients   │
│ • Reviews      │  │ • Instructions  │
└────────────────┘  └─────────────────┘
```

## ✨ Key Features

### 1. Hybrid Data Model
- **Search:** Live queries to TheCocktailDB API for comprehensive recipe database
- **Lazy-Saving:** When users favorite a drink, external data is captured and persisted locally to reduce API calls
- **Smart Caching:** Eliminates redundant API requests for frequently accessed recipes

### 2. Social Engine
- Full review system with 1-5 star ratings
- User comments and feedback on recipes
- Dynamic calculation of average ratings and review counts
- User-specific favorites list

### 3. DevOps & Deployment
- **Automated CI/CD Pipeline:** GitHub Actions orchestrates testing and deployment
- **Zero-Downtime Deployment:** Blue-green deployment strategy with Docker
- **Infrastructure as Code:** Docker Compose defines entire stack
- **Production Serving:** Gunicorn behind Nginx for security and performance

### 4. Responsive UI
- Mobile-first design with Bootstrap 5
- Seamless experience across all devices
- Intuitive recipe browsing and management

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.9+ (for manual installation)
- PostgreSQL 15+ (for manual installation)

### Docker Setup (Recommended)

**1. Clone the Repository**
```bash
git clone https://github.com/AsHkAn-Django/drink-recipe-finder.git
cd drink-recipe-finder
```

**2. Configure Environment**
Create a `.env` file in the root directory:
```env
# Django Configuration
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=cocktail_db
DB_USER=recipe_user
DB_PASSWORD=MySimplePass123
DB_HOST=db
```

**3. Launch the Application**
```bash
docker compose up -d --build
```

**4. Initialize Database**
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
```

**5. Access the Application**
Open your browser and navigate to: `http://localhost:8003`

### Manual Installation (Local Development)

**1. Create Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure Environment**
Create a `.env` file with the same configuration as above (adjust `DB_HOST` to `localhost`).

**4. Setup Database & Run Server**
```bash
python manage.py migrate
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 🧪 Testing

This project emphasizes quality through comprehensive automated testing.

### Testing Strategy

**Unit Tests:** Validate data models (Recipe, Review) and custom methods
**Integration Tests:** Verify view logic, permissions, and HTTP redirects
**API Mocking:** Uses `unittest.mock` to simulate external API responses

### Benefits of Mocked Tests
- ⚡ **Fast:** No network overhead
- 🔒 **Reliable:** Tests pass even if external API is unavailable
- 🎯 **Deterministic:** Complete control over test data and edge cases

### Running Tests

```bash
# Run all tests
docker compose exec web pytest

# Run with coverage report
docker compose exec web pytest --cov

# Run specific test file
docker compose exec web pytest tests/test_views.py

# Run tests locally (without Docker)
pytest
```

## 📡 API Documentation

The application exposes RESTful endpoints for integration and programmatic access.

### Recipe Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|-----------------|
| `GET` | `/api/v1/recipes/` | List all saved recipes | Required |
| `GET` | `/api/v1/recipes/?search=margarita` | Search recipes by title | Required |
| `GET` | `/api/v1/recipes/{id}/` | Retrieve recipe details | Required |

### Favorites Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|-----------------|
| `POST` | `/api/v1/favorites/` | Add recipe to favorites | Required |
| `DELETE` | `/api/v1/favorites/{id}/` | Remove from favorites | Required |
| `GET` | `/api/v1/favorites/` | List user's favorites | Required |

### Review Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|-----------------|
| `POST` | `/api/v1/reviews/` | Create a review | Required |
| `GET` | `/api/v1/reviews/?recipe={id}` | Get reviews for recipe | Optional |
| `PUT` | `/api/v1/reviews/{id}/` | Update review | Owner only |
| `DELETE` | `/api/v1/reviews/{id}/` | Delete review | Owner only |

### Example Request

```bash
# Search for margarita recipes
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8003/api/v1/recipes/?search=margarita"

# Add to favorites
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"recipe_id": 12345}' \
  "http://localhost:8003/api/v1/favorites/"
```

## 🔧 CI/CD Pipeline

Every push to `main` triggers an automated workflow:

1. **Code Quality Checks**
   - Flake8: Linting and style verification
   - Black: Code formatting consistency

2. **Testing Suite**
   - Full Pytest coverage
   - Model, view, and API integration tests
   - Edge case validation

3. **Deployment** (on success)
   - SSH into production VPS
   - Pull latest code
   - Rebuild Docker containers
   - Run migrations with zero downtime
   - Health checks


## 🔐 Security & Production Best Practices

- **Environment Variables:** Sensitive data (SECRET_KEY, DB credentials) stored in `.env`
- **Debug Mode:** Disabled in production
- **Gunicorn:** Application server with worker process management
- **Nginx:** Reverse proxy with SSL termination and security headers
- **Database:** PostgreSQL 15 with user permissions and encrypted connections
- **CSRF Protection:** Enabled for all state-changing operations
- **Dependency Management:** Regular updates and security scanning


## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

**Made with ❤️ by Aman Jha**