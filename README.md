# 🚀 Exemplar Prompt Hub

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test Coverage](https://img.shields.io/badge/test%20coverage-100%25-brightgreen)](tests/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.24.0-red)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](docker-compose.yml)

A modern REST API service for managing and serving AI prompts. This service provides a centralized repository for storing, versioning, and retrieving prompts for various AI applications. It uses PostgreSQL as the database for robust and scalable data management.

## ✨ Features

For a detailed checklist of implemented and planned features, see [FEATURES.md](FEATURES.md).

- **RESTful API** for prompt management
- **Version control** for prompts
- **Tag-based prompt organization**
- **Metadata support** for prompts
- **Authentication and authorization**
- **Search and filtering capabilities**

## 🛠️ Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- PostgreSQL (for database)
- Docker and Docker Compose (for containerized setup)

### Quick Start with Docker

The easiest way to get started is using Docker Compose:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/exemplar-prompt-hub.git
   cd exemplar-prompt-hub
   ```

2. **Start the services:**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - FastAPI backend at http://localhost:8000
   - PostgreSQL database at localhost:5432
   - Streamlit UI at http://localhost:8501

3. **Access the services:**
   - API Documentation: http://localhost:8000/docs
   - Streamlit UI: http://localhost:8501

4. **Stop the services:**
   ```bash
   docker-compose down
   ```

### Manual Installation

If you prefer to run the services manually:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/exemplar-prompt-hub.git
   cd exemplar-prompt-hub
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` to configure your database and other settings.

5. **Start the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Running Tests
To run the tests, use:
```bash
pytest
```

For detailed test coverage, use:
```bash
pytest --cov=app --cov-report=term-missing
```

### Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For detailed contribution guidelines, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📁 Project Structure

```
exemplar-prompt-hub/
├── app/
│   ├── api/             # API endpoints
│   ├── core/            # Core functionality
│   ├── db/              # Database models and session
│   ├── schemas/         # Pydantic models
│   └── main.py          # Application entry point
├── tests/               # Test files
├── .env                 # Environment variables
├── .env.example         # Example environment variables
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## 📊 Database Table Structure

The application uses the following database tables:

### Prompts Table
- **id**: Integer (Primary Key)
- **name**: String (Unique)
- **text**: String
- **description**: String
- **version**: Integer
- **meta**: JSON
- **created_at**: DateTime
- **updated_at**: DateTime

### Tags Table
- **id**: Integer (Primary Key)
- **name**: String (Unique)

### PromptVersions Table
- **id**: Integer (Primary Key)
- **prompt_id**: Integer (Foreign Key to Prompts)
- **version**: Integer
- **text**: String
- **meta**: JSON
- **created_at**: DateTime

## 🔄 Updating Prompts with Versioning

To update a prompt with versioning, follow these steps:

1. **Retrieve the Prompt:**
   Use the `GET /api/v1/prompts/{prompt_id}` endpoint to retrieve the prompt you want to update.

2. **Update the Prompt:**
   Use the `PUT /api/v1/prompts/{prompt_id}` endpoint to update the prompt. You can include the following fields:
   - **name**: (Optional) The new name of the prompt.
   - **text**: (Optional) The new text of the prompt.
   - **description**: (Optional) The new description of the prompt.
   - **version**: (Optional) The new version number.
   - **meta**: (Optional) Any additional metadata.

3. **Versioning Logic:**
   - If you provide a new version number, the system will create a new entry in the `PromptVersions`