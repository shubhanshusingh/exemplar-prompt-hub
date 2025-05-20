# 🚀 Exemplar Prompt Hub

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test Coverage](https://img.shields.io/badge/test%20coverage-100%25-brightgreen)](tests/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](docker-compose.yml)

A modern REST API service for managing and serving AI prompts. This service provides a centralized repository for storing, versioning, and retrieving prompts for various AI applications. It uses PostgreSQL as the database for robust and scalable data management.

---

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
- PostgreSQL (for database) (by default it uses sqlite as per .env.example)
- Docker and Docker Compose (for containerized setup)

### Installation

#### Using pip

You can install the package directly from PyPI:

### 🐍 Python (pip, Virtual Environment)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install exemplar-prompt-hub
# Create a .env file and copy content from .env.example as per the github repo
cp .env.example .env
# Edit .env as needed
prompt-hub
```

Or install from the source:

```bash
# Clone the repository
git clone https://github.com/yourusername/exemplar-prompt-hub.git
cd exemplar-prompt-hub

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the package
pip install -e .

# Copy .env.example to .env [copy .env.example from github repo branch]
cp .env.example .env

# Edit .env to configure your database and other settings
```

After installation, you can use the following command:
- `prompt-hub` - Start the FastAPI server

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

3. **Access the services:**
   - API Documentation: http://localhost:8000/docs

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
curl "http://localhost:8000/api/v1/prompts/{prompt_id}"
```

### Update a Prompt
```bash
curl -X PUT "http://localhost:8000/api/v1/prompts/{prompt_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated prompt text",
    "description": "Updated description",
    "meta": {
      "author": "test-user",
      "category": "updated"
    },
    "tags": ["updated", "test"]
  }'
```

### Delete a Prompt
```bash
curl -X DELETE "http://localhost:8000/api/v1/prompts/{prompt_id}"
```

## 📁 Project Structure

```
exemplar-prompt-hub/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── prompts.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── base_class.py
│   │   ├── models.py
│   │   └── session.py
│   ├── schemas/
│   │   └── prompt.py
│   └── main.py
├── tests/
│   └── test_prompts.py
├── alembic/
│   └── versions/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── MANIFEST.in
├── pyproject.toml
├── README.md
├── requirements.txt
└── setup.py
```

## 📊 Database Table Structure

### Prompts Table
```sql
CREATE TABLE prompts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    description TEXT,
    version INTEGER NOT NULL,
    meta JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Tags Table
```sql
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);
```

### Prompt Tags Table (Many-to-Many Relationship)
```sql
CREATE TABLE prompt_tags (
    prompt_id INTEGER REFERENCES prompts(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (prompt_id, tag_id)
);
```

## 🔄 Updating Prompts with Versioning

The API supports versioning of prompts. When updating a prompt:

1. The current version is incremented
2. A new record is created with the updated content
3. The old version is preserved for reference

To update a prompt, use the PUT endpoint with the prompt ID:

```bash
curl -X PUT "http://localhost:8000/api/v1/prompts/{prompt_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated prompt text",
    "description": "Updated description",
    "meta": {
      "author": "test-user",
      "category": "updated"
    },
    "tags": ["updated", "test"]
  }'
```

The API will automatically handle versioning and maintain the history of changes.

## 🎨 Using Prompts with Jinja Templating

The API supports Jinja2 templating in prompts, allowing you to create dynamic prompts with variables. Here's how to use it:

### 1. Create a Template Prompt

```bash
curl -X POST "http://localhost:8000/api/v1/prompts/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "greeting-template",
    "text": "Hello {{ name }}! Welcome to {{ platform }}. Your role is {{ role }}.",
    "description": "A greeting template with dynamic variables",
    "meta": {
      "template_variables": ["name", "platform", "role"],
      "author": "test-user"
    },
    "tags": ["template", "greeting"]
  }'
```

### 2. Use the Template in Python

```python
import requests
import jinja2
from jinja2 import Template

# Fetch the prompt template
response = requests.get("http://localhost:8000/api/v1/prompts/{prompt_id}")
prompt_data = response.json()

# Create a Jinja template
template = Template(prompt_data["text"])

# Render with variables
rendered_prompt = template.render(
    name="John",
    platform="Exemplar Prompt Hub",
    role="Developer"
)

print(rendered_prompt)
# Output: Hello John! Welcome to Exemplar Prompt Hub. Your role is Developer.
```

### 3. Advanced Template Features

You can use all Jinja2 features in your prompts:

```bash
# Create a prompt with Jinja2 control structures
curl -X POST "http://localhost:8000/api/v1/prompts/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "advanced-template",
    "text": "{% if user_type == \"admin\" %}Welcome, Administrator!{% else %}Welcome, User!{% endif %}\n\n{% for item in features %}- {{ item }}\n{% endfor %}",
    "description": "Advanced template with control structures",
    "meta": {
      "template_variables": ["user_type", "features"],
      "author": "test-user"
    },
    "tags": ["template", "advanced"]
  }'
```

### 4. Template with Filters

```python
# Fetch and render a template with filters
response = requests.get("http://localhost:8000/api/v1/prompts/{prompt_id}")
prompt_data = response.json()

template = Template(prompt_data["text"])
rendered_prompt = template.render(
    user_type="admin",
    features=["Version Control", "Templating", "API Access"]
)

print(rendered_prompt)
# Output:
# Welcome, Administrator!
#
# - Version Control
# - Templating
# - API Access
```

### 5. Template with Macros

```bash
# Create a prompt with Jinja2 macros
curl -X POST "http://localhost:8000/api/v1/prompts/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "macro-template",
    "text": "{% macro format_item(item) %}- {{ item|title }}\n{% endmacro %}\n\n{% for category in categories %}{{ category.name }}:\n{% for item in category.items %}{{ format_item(item) }}{% endfor %}\n{% endfor %}",
    "description": "Template using Jinja2 macros",
    "meta": {
      "template_variables": ["categories"],
      "author": "test-user"
    },
    "tags": ["template", "macro"]
  }'
```

### Best Practices

1. **Document Variables**: Always document template variables in the prompt's meta field
2. **Default Values**: Consider providing default values in the template
3. **Error Handling**: Use Jinja2's error handling features
4. **Security**: Be careful with user input in templates
5. **Versioning**: Use the API's versioning feature to track template changes

### Example with Error Handling

```python
from jinja2 import Template, TemplateError

try:
    template = Template(prompt_data["text"])
    rendered_prompt = template.render(
        name="John",
        platform="Exemplar Prompt Hub"
        # role is missing, will use default if defined
    )
except TemplateError as e:
    print(f"Template error: {e}")
```

This templating system allows you to create dynamic, reusable prompts while maintaining version control and easy management through the API.