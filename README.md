# Lernex - Digital Learning Marketplace API

[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue)](https://github.com/username/lernex-api)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)](https://fastapi.tiangolo.com/)
[![Coverage](https://img.shields.io/badge/Coverage-%3E95%25-brightgreen)](https://github.com/username/lernex-api)

Production-ready FastAPI microservice for a Digital Learning Marketplace. Enables learners to register, explore courses, enroll, track progress, and provide feedback.

---

## Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Overview](#-api-overview)
- [Application Workflow](#-application-workflow)
- [Data Models](#-data-models)
- [Examples](#-examples)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Author](#-author)

---

## Features

- **User Authentication**: JWT-based authentication with secure login and registration
- **Course Management**: Browse, explore, and view detailed course information
- **Enrollment System**: Enroll in courses with status tracking (ACTIVE, COMPLETED, CANCELLED)
- **Progress Tracking**: Monitor learning progress with completion rates
- **Feedback System**: Submit ratings and comments for courses
- **Recommendations**: AI-powered course recommendations
- **RESTful API**: Clean, well-documented API endpoints
- **Docker Support**: Containerized deployment ready
- **High Test Coverage**: >95% code coverage with comprehensive tests
- **CI/CD Pipeline**: Automated testing and deployment via GitHub Actions

---

## Quick Start

### Docker Usage

```bash
# Build the Docker image
docker build -t lernex-api .

# Run the container
docker run -d -p 8000:80 --name lernex-container lernex-api
```

**Access the application:**
- App: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs

### Local Development

#### 1. Clone the repository

```bash
git clone https://github.com/username/lernex-api.git
cd lernex-api
```

#### 2. Create a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run the application

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at http://localhost:8000

#### 5. Run tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## Project Structure

```
lernex-api/
├── .github/
│   └── workflows/
│       └── ci.yml              
├── app/
│   ├── api/
│   │   ├── auth_router.py     
│   │   ├── course_router.py    
│   │   ├── enrollment_router.py
│   │   ├── feedback_router.py
│   │   ├── progress_router.py
│   │   └── recommendation_router.py
│   ├── domain/
│   │   ├── course.py          
│   │   ├── user.py             
│   │   ├── enrollment.py
│   │   ├── feedback.py
│   │   └── progress.py
│   ├── main.py                 
│   └── storage.py            
├── tests/
│   ├── test_auth.py
│   ├── test_courses.py
│   └── ...
├── Dockerfile                  
├── requirements.txt            
└── README.md                    
```

---

## API Overview

All endpoints use JSON format for request and response bodies.

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register a new learner | No |
| POST | `/auth/login` | Login and receive JWT token | No |
| GET | `/auth/me` | Get current user profile | Yes |

### Course Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/courses/` | List all available courses | Yes |
| GET | `/courses/{id}` | Get course details | Yes |
| GET | `/courses/my-courses` | List enrolled courses | Yes |
| POST | `/courses/{id}/enroll` | Enroll in a course | Yes |

### Learning Management Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/feedback/` | Submit course feedback | Yes |
| POST | `/progress/` | Update learning progress | Yes |
| POST | `/recommendations/` | Get course recommendations | Yes |

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Bad request (e.g., email already registered, already enrolled) |
| 401 | Unauthorized (invalid or missing token) |
| 404 | Resource not found (course or learner) |
| 422 | Validation error (invalid request body) |
| 500 | Internal server error |

---

## Application Workflow

The typical learner lifecycle follows this flow:

```
REGISTER → LOGIN → EXPLORE → ENROLL → LEARN & TRACK
```

1. **REGISTER**: Create a new learner account with email and password
2. **LOGIN**: Authenticate to receive a JWT access token
3. **EXPLORE**: Browse available courses and view detailed information
4. **ENROLL**: Join a course (enrollment status becomes ACTIVE)
5. **LEARN & TRACK**: Update progress, submit feedback, and complete courses

---

## Data Models

### Course

```python
{
  "course_id": "str (UUID)",
  "title": "str",
  "description": "str",
  "instructor_id": "str",
  "modules": "List[CourseModule]",
  "detail": "CourseDetail",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Learner

```python
{
  "learner_id": "str (UUID)",
  "name": "str",
  "email": "EmailStr",
  "join_date": "datetime",
  "profile": "Profile"
}
```

### Enrollment

```python
{
  "enrollment_id": "str (UUID)",
  "learner_id": "str",
  "course_id": "str",
  "enrollment_date": "datetime",
  "status": "str (ACTIVE | COMPLETED | CANCELLED)"
}
```

### Feedback

```python
{
  "feedback_id": "str (UUID)",
  "learner_id": "str",
  "course_id": "str",
  "comment": "str",
  "rating": {
    "value": "int (1-5)",
    "comment_category": "str"
  },
  "submitted_at": "datetime"
}
```

### Progress

```python
{
  "progress_id": "str (UUID)",
  "learner_id": "str",
  "course_id": "str",
  "completion_rate": "float (0.0-1.0)",
  "status": "str (NOT_STARTED | IN_PROGRESS | COMPLETED)",
  "last_accessed": "datetime"
}
```

---

## Examples

### Register a New Learner

**Request:**
```json
POST /auth/register
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "learner_id": "l-uuid-123",
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Learner registered successfully. You can now login."
}
```

### Login

**Request:**
```json
POST /auth/login
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer",
  "learner_id": "l-uuid-123",
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Get Available Courses

**Request:**
```bash
GET /courses/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR...
```

**Response:**
```json
[
  {
    "course_id": "course-001",
    "title": "Python Fundamentals",
    "description": "Learn Python basics from scratch",
    "instructor_id": "instr-001",
    "instructor_name": "John Doe",
    "total_modules": 1,
    "total_lessons": 1,
    "total_topics": 2
  }
]
```

### Submit Course Feedback

**Request:**
```json
POST /feedback/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR...
{
  "learner_id": "learner-123",
  "course_id": "course-001",
  "comment": "Excellent course structure!",
  "rating": {
    "value": 5,
    "comment_category": "content"
  }
}
```

### Update Learning Progress

**Request:**
```json
POST /progress/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR...
{
  "learner_id": "learner-123",
  "course_id": "course-001",
  "completion_rate": 0.75,
  "status": "IN_PROGRESS"
}
```

---

## Testing

The project includes comprehensive test coverage (>95%) for all endpoints and business logic.

### Run Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run tests with coverage report
pytest --cov=app --cov-report=term-missing

# Run tests with HTML coverage report
pytest --cov=app --cov-report=html
```

### Test Structure

```
tests/
├── test_auth.py          
├── test_courses.py      
├── test_enrollment.py  
├── test_feedback.py       
└── test_progress.py      
```

---

## Deployment

### Live Demo (Railway)

The application is deployed on Railway with automatic deployments on every push to the `main` branch.

- **Base URL**: https://ii3160-tugas-besar-lernex-production.up.railway.app
- **Interactive API Documentation**: https://ii3160-tugas-besar-lernex-production.up.railway.app/docs

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

- **Automated Testing**: Runs on every push and pull request
- **Code Linting**: Flake8 checks for code quality
- **Docker Build**: Validates Docker image creation
- **Auto Deploy**: Deploys to Railway on successful builds

View the CI/CD configuration in `.github/workflows/ci.yml`

### Docker Deployment

```bash
# Build the image
docker build -t lernex-api .

# Run the container
docker run -d -p 8000:80 --name lernex-container lernex-api

# View logs
docker logs lernex-container

# Stop the container
docker stop lernex-container

# Remove the container
docker rm lernex-container
```

---

## 📝 Development

### Setting Up Development Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server with auto-reload
uvicorn app.main:app --reload --port 8000

# Run tests in watch mode
pytest-watch
```

### Code Quality

```bash
# Format code
black app/ tests/

# Check code style
flake8 app/ tests/

# Type checking
mypy app/
```

---

## Author

<div align="center">
  <img src="https://github.com/StefanyJosefina.png" width="100" style="border-radius: 50%;" alt="Stefany Josefina Santono"/>
  
  **Stefany Josefina Santono**  
  Student ID: 18223116
  
  [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/StefanyJosefina)
</div>

---
