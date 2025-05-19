# Exemplar Prompt Hub

A modern REST API service for managing and serving AI prompts. This service provides a centralized repository for storing, versioning, and retrieving prompts for various AI applications.

## Features

- RESTful API for prompt management
- Version control for prompts
- Tag-based prompt organization
- Metadata support for prompts
- Authentication and authorization
- Search and filtering capabilities

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

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

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the application:**
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
Contributions are welcome! Please feel free to submit a Pull Request.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
exemplar-prompt-hub/
├── alembic/              # Database migrations
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