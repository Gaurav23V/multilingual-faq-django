# Multilingual FAQ System

A Django-based application that provides a multilingual FAQ (Frequently Asked Questions) system with support for automatic translations, caching, WYSIWYG editor integration, and a RESTful API. The application supports English, Hindi, and Bengali languages and can be easily extended to support more languages.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [Running the Application](#running-the-application)
  - [Running Locally](#running-locally)
  - [Running with Docker](#running-with-docker)
- [Running Tests](#running-tests)
- [API Usage](#api-usage)
  - [Endpoints](#endpoints)
  - [Examples](#examples)
- [License](#license)

---

## Features

- **Multilingual Support**: Automatic translation of FAQs into Hindi and Bengali using Google Translate API.
- **RESTful API**: Provides endpoints to retrieve FAQs with language selection.
- **Caching Mechanism**: Uses Redis to cache translations for improved performance.
- **Admin Interface**: User-friendly Django admin panel with WYSIWYG editor support for managing FAQs.
- **WYSIWYG Editor**: Integrates `django-ckeditor` for rich text formatting of answers.
- **Test Coverage**: Comprehensive unit tests with 93% coverage using pytest.

## Technologies Used

- **Python 3.10**
- **Django 5.0.2**
- **Django REST Framework**
- **Redis**
- **Docker**
- **pytest**
- **django-ckeditor**
- **googletrans**

---

## Installation

### Prerequisites

- **Python 3.10**
- **pip**
- **Docker (optional, for Docker setup)**
- **Redis (if running locally without Docker)**

### Local Setup

Follow these steps to set up the project locally on your machine:

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/multilingual-faq-system.git
cd multilingual-faq-system
```

#### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

- On Linux/Mac:

  ```bash
  source venv/bin/activate
  ```

- On Windows:

  ```bash
  venv\Scripts\activate
  ```

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://127.0.0.1:6379/1
```

- Replace `your-secret-key` with a securely generated key.
- Ensure Redis is running locally on your machine.

#### 5. Apply Migrations

```bash
python manage.py migrate
```

#### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

---

### Docker Setup

You can run the application in a Docker container, which also sets up Redis.

#### 1. Build and Run the Containers

```bash
docker-compose build
docker-compose up
```

#### 2. Create a Superuser in Docker

In a new terminal:

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## Running the Application

### Running Locally

Start the development server:

```bash
python manage.py runserver
```

Access the application at `http://localhost:8000/`.

### Running with Docker

The application will be accessible at `http://localhost:8000/` once the containers are up.

---

## Running Tests

Ensure that you have the virtual environment activated and the dependencies installed.

### Running All Tests

```bash
pytest
```

### Viewing Coverage Report

Generate an HTML coverage report:

```bash
pytest --cov=faqs --cov-report=html
```

Open `htmlcov/index.html` in your browser to view the coverage report.

- **Test Coverage**: The application has a test coverage of **93%**, ensuring reliability and correctness.

---

## API Usage

### Endpoints

- **List FAQs**: `/api/faqs/`
- **Retrieve Single FAQ**: `/api/faqs/<id>/`

### Parameters

- **`lang`**: Optional query parameter to specify the language (`en`, `hi`, `bn`). Defaults to `en`.

### Examples

#### Fetch FAQs in English (Default)

```bash
curl http://localhost:8000/api/faqs/
```

#### Fetch FAQs in Hindi

```bash
curl http://localhost:8000/api/faqs/?lang=hi
```

#### Fetch FAQs in Bengali

```bash
curl http://localhost:8000/api/faqs/?lang=bn
```

#### Fetch a Single FAQ in English

```bash
curl http://localhost:8000/api/faqs/1/
```

#### Fetch a Single FAQ in Hindi

```bash
curl http://localhost:8000/api/faqs/1/?lang=hi
```

#### Example Response

```json
[
  {
    "id": 1,
    "question": "What is this service?",
    "answer": "<p>This is a test service.</p>",
    "created_at": "2023-10-01T12:00:00Z",
    "updated_at": "2023-10-01T12:00:00Z"
  }
]
```

## Project Overview

### Purpose

The Multilingual FAQ System is designed to:

- Provide a flexible FAQ system with support for multiple languages.
- Automatically translate content, reducing the manual effort required.
- Offer a RESTful API for easy integration with front-end applications.

### Architectural Decisions

- **Django**: Chosen for its robustness and ease of development.
- **Django REST Framework**: Provides powerful tools for building APIs.
- **Redis**: Used for caching to improve performance.
- **docker-compose**: Simplifies the development environment setup.

### Technologies Used

- **Python 3.10**
- **Django 5.0.2**
- **Django REST Framework**
- **Redis**
- **Docker**
- **pytest**
- **django-ckeditor**
- **googletrans**

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

If you have any questions or need further assistance, feel free to open an issue or contact the maintainer.

**Happy Coding!**