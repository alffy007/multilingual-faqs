# FAQ Management System

## Overview

The **FAQ Management System** is a Django-based web application designed for handling frequently asked questions (FAQs) with multilingual support and efficient caching mechanisms. It allows businesses or services to manage FAQs in multiple languages and provides an admin interface for easy management. The application is Dockerized for easy deployment and supports caching for better performance.

## Key Features

- **Multilingual Support**: FAQ content can be translated into multiple languages.
- **Caching**: Translations are cached for faster retrieval, reducing the load on the database.
- **Admin Interface**: Customizable Django Admin for managing FAQs.
- **Docker Support**: Dockerized application for easy deployment.
- **Unit Testing**: Comprehensive test suite ensuring application correctness.
- **REST API**: Exposes API endpoints for managing FAQs programmatically.

## Requirements

- Python 3.11+
- Django 4.x
- PostgreSQL
- Redis (for caching)
- Docker (for containerization)
- Render account (for deployment)

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/alffy007/multilingual-faqs
cd multilingual-faqs
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install the required dependencies

```bash
pip install -r requirements.txt
```


### 4. Run database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser for Django Admin

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Access the app at [http://localhost:8000](http://localhost:8000).

## API Endpoints

The FAQ Management System provides a RESTful API for managing FAQs. Below are the available endpoints:

### 1. Get FAQs

```http
GET /api/faqs/
```
#### Response
```json
[
  {
    "question": "will there be accomadation",
    "answer": "\u003Cp\u003EYes, There will be accomadation\u003C/p\u003E"
  },
    "question": "what will be the price?",
    "answer": "almost 2"
  },
  {
    "question": "what about tommorrow?",
    "answer": "\u003Cp\u003Efine\u003C/p\u003E"
  }
]
```

### 2. Get a Specific Language FAQ

```http
GET /api/faqs/?lang={language}/
```
languages configured = hi, bn, ml (ps: Easy to add new languages)
#### Response
```json
[
  {
    "question": "कीमत क्या होगी?",
    "answer": "लगभग 2"
  },
  {
    "question": "Django क्या है?",
    "answer": "\u003Cp\u003E एक पायथन फ्रेमवर्क \u003C/p\u003E"
  },
  {
    "question": "फास्टपी क्या है?",
    "answer": "\u003Cp\u003E एक पायथन फ्रेमवर्क \u003C/p\u003E"
  }
]
```

### 3. Create New FAQ

```http
POST /api/faqs/
```
#### Request Body
```json
{
  "question_en": "How does caching work?",
  "answer_en": "Caching improves performance by storing translations for quick access."
}
```
#### Response
```json
{

  "question_en": "How does caching work?",
  "answer_en": "Caching improves performance by storing translations for quick access.",
  "translations": {(translating in background and update automaticaly)},
  "is_updated": true
}
```

### 4. Update an FAQ

```http
PUT /api/faqs/{id}/
```
#### Request Body
```json
{
  "question_en": "How does the caching system work?",
  "answer_en": "It speeds up access by reducing redundant translation requests."
}
```
#### Response
```json
{
  "question_en": "How does the caching system work?",
  "answer_en": "It speeds up access by reducing redundant translation requests.",
  "translations": {},
  "is_updated": true
}
```

### 5. Delete an FAQ

```http
DELETE /api/faqs/{id}/
```
#### Response
```json
{
  "message": "FAQ deleted successfully."
}
```

## Docker Support

### 1. Build the Docker image

```bash
docker build -t faq-management-system .
```

### 2. Run the application using Docker Compose

```bash
docker-compose up
```

### 3. Docker Compose File

```yaml
version: '3'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: bharath_fd_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: bharath_fd
    restart: always  
    ports:
      - 5432:5432
    volumes:
      - db_data:/var/lib/postgresql/data

  web:
    restart: always
    build: .
    volumes:
      - .:/app
    ports:
      - "80:80"
    depends_on:
      - db
  redis:
    image: "redis"
    ports:
      - "6379:6379"    
    volumes:
      - redis_data:/data  

volumes:
  db_data:
  redis_data:

```

## Deployment to Render

Follow the [Render Deployment Guide](https://render.com/docs/deploying-docker-containers) to deploy your FAQ Management System with ease.

## Testing

Run the test suite to validate the system:

```bash
pytest
```

With seamless deployment, efficient functionality, and clear documentation, this FAQ Management System is ready to scale and serve your needs—making your FAQ handling smarter, faster, and more reliable. 🚀

