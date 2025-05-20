# 🚀 Exemplar Prompt Hub

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test Coverage](https://img.shields.io/badge/test%20coverage-100%25-brightgreen)](tests/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.24.0-red)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](docker-compose.yml)

## 📑 Table of Contents

- [Features](#-features)
- [Getting Started](#️-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Quick Start with Docker](#quick-start-with-docker)
  - [Manual Installation](#manual-installation)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)
- [API Documentation](#-api-documentation)
- [API Usage Examples](#-api-usage-examples)
- [Project Structure](#-project-structure)
- [Database Table Structure](#-database-table-structure)
- [Updating Prompts with Versioning](#-updating-prompts-with-versioning)

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

### Installation

#### Using pip

You can install the package directly from PyPI:

```bash
pip install exemplar-prompt-hub
```

Or install from the source:

```bash
# Clone the repository
git clone https://github.com/yourusername/exemplar-prompt-hub.git
cd exemplar-prompt-hub

# Install the package
pip install -e .
```

After installation, you can use the following commands:
- `prompt-hub` - Start the FastAPI server
- `prompt-hub-ui` - Start the Streamlit UI

#### Using Docker

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

## 🔄 API Usage Examples

Here are some example curl commands to interact with the API:

### Create a Prompt
```bash
curl -X POST "http://localhost:8000/api/v1/prompts/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "example-prompt",
    "text": "This is an example prompt text",
    "description": "A sample prompt for demonstration",
    "version": 1,
    "meta": {
      "author": "test-user",
      "category": "example"
    },
    "tags": ["example", "test"]
  }'
```

### Get All Prompts
```bash
# Get all prompts
curl "http://localhost:8000/api/v1/prompts/"

# Get prompts with search
curl "http://localhost:8000/api/v1/prompts/?search=example"

# Get prompts with tag filter
curl "http://localhost:8000/api/v1/prompts/?tag=test"

# Get prompts with pagination
curl "http://localhost:8000/api/v1/prompts/?skip=0&limit=10"
```

### Get a Specific Prompt
```bash
# Replace {prompt_id} with actual ID
curl "http://localhost:8000/api/v1/prompts/1"
```

### Update a Prompt
```bash
# Replace {prompt_id} with actual ID
curl -X PUT "http://localhost:8000/api/v1/prompts/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "updated-example-prompt",
    "text": "This is the updated prompt text",
    "description": "Updated description",
    "version": 2,
    "meta": {
      "author": "test-user",
      "category": "example",
      "updated": true
    },
    "tags": ["example", "test", "updated"]
  }'
```

### Delete a Prompt
```bash
# Replace {prompt_id} with actual ID
curl -X DELETE "http://localhost:8000/api/v1/prompts/1"
```

### Complete Flow Example
Here's a complete flow example using a single prompt:

```bash
# 1. Create a new prompt
CREATE_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/prompts/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "flow-example",
    "text": "Initial prompt text",
    "description": "Example for complete flow",
    "version": 1,
    "meta": {"author": "test-user"},
    "tags": ["flow", "example"]
  }')

# Extract prompt ID from response
PROMPT_ID=$(echo $CREATE_RESPONSE | jq -r '.id')

# 2. Get the created prompt
curl "http://localhost:8000/api/v1/prompts/$PROMPT_ID"

# 3. Update the prompt
curl -X PUT "http://localhost:8000/api/v1/prompts/$PROMPT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated prompt text",
    "description": "Updated description",
    "version": 2,
    "meta": {"author": "test-user", "updated": true},
    "tags": ["flow", "example", "updated"]
  }'

# 4. Get the updated prompt
curl "http://localhost:8000/api/v1/prompts/$PROMPT_ID"

# 5. Delete the prompt
curl -X DELETE "http://localhost:8000/api/v1/prompts/$PROMPT_ID"

# 6. Verify deletion
curl "http://localhost:8000/api/v1/prompts/$PROMPT_ID"
```

Note: The complete flow example requires `jq` to be installed for JSON parsing. You can install it using:
- Ubuntu/Debian: `sudo apt-get install jq`
- macOS: `brew install jq`
- Windows: Download from https://stedolan.github.io/jq/download/

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