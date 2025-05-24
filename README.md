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
    "meta": {
      "author": "test-user",
      "category": "example"
    },
    "tags": ["example", "test"]
  }'
```

Note: The `version` field is optional and handled automatically by the API. New prompts start with version 1, and subsequent updates will increment the version number automatically.

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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    text TEXT NOT NULL,
    description TEXT,
    version INTEGER NOT NULL,
    meta TEXT,  -- Store JSON as TEXT in SQLite
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Tags Table
```sql
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
```

### Prompt Tags Table (Many-to-Many Relationship)
```sql
CREATE TABLE prompt_tags (
    prompt_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (prompt_id, tag_id),
    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
```

### Prompt Versions Table
```sql
CREATE TABLE prompt_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER,
    version INTEGER,
    text TEXT,
    description TEXT,
    meta TEXT,  -- Store JSON as TEXT in SQLite
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE
);
```

### Indexes
```sql
CREATE INDEX idx_prompts_name ON prompts(name);
CREATE INDEX idx_tags_name ON tags(name);
CREATE INDEX idx_prompt_versions_prompt_id ON prompt_versions(prompt_id);
CREATE INDEX idx_prompt_tags_prompt_id ON prompt_tags(prompt_id);
CREATE INDEX idx_prompt_tags_tag_id ON prompt_tags(tag_id);
```

### Timestamp Trigger
```sql
CREATE TRIGGER update_prompt_timestamp 
AFTER UPDATE ON prompts
BEGIN
    UPDATE prompts SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;
```

Key differences from PostgreSQL:
1. Uses `INTEGER PRIMARY KEY AUTOINCREMENT` instead of `SERIAL`
2. Uses `TEXT` instead of `VARCHAR` and `JSONB`
3. Stores JSON as `TEXT` with manual serialization
4. Requires explicit foreign key support with `PRAGMA foreign_keys = ON`
5. Uses triggers for `updated_at` timestamp management

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
# Create a basic greeting template
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

# Response:
{
  "id": 1,
  "name": "greeting-template",
  "text": "Hello {{ name }}! Welcome to {{ platform }}. Your role is {{ role }}.",
  "description": "A greeting template with dynamic variables",
  "version": 1,
  "meta": {
    "template_variables": ["name", "platform", "role"],
    "author": "test-user"
  },
  "tags": [
    {"id": 1, "name": "template"},
    {"id": 2, "name": "greeting"}
  ],
  "created_at": "2024-03-20T10:00:00",
  "updated_at": null
}
```

See [examples/jinja_open_ai.py](examples/jinja_open_ai.py) for a complete Python implementation of how to use this template with Jinja2.


### 2. Fetch and Use Templates

```bash
# Fetch a template by ID
curl "http://localhost:8000/api/v1/prompts/1"

# Response:
{
  "id": 1,
  "name": "greeting-template",
  "text": "Hello {{ name }}! Welcome to {{ platform }}. Your role is {{ role }}.",
  "description": "A greeting template with dynamic variables",
  "version": 1,
  "meta": {
    "template_variables": ["name", "platform", "role"],
    "author": "test-user"
  },
  "tags": [
    {"id": 1, "name": "template"},
    {"id": 2, "name": "greeting"}
  ],
  "created_at": "2024-03-20T10:00:00",
  "updated_at": null
}

# Fetch a template by name
curl "http://localhost:8000/api/v1/prompts/?search=greeting-template"

# Response:
[
  {
    "id": 1,
    "name": "greeting-template",
    "text": "Hello {{ name }}! Welcome to {{ platform }}. Your role is {{ role }}.",
    "description": "A greeting template with dynamic variables",
    "version": 1,
    "meta": {
      "template_variables": ["name", "platform", "role"],
      "author": "test-user"
    },
    "tags": [
      {"id": 1, "name": "template"},
      {"id": 2, "name": "greeting"}
    ],
    "created_at": "2024-03-20T10:00:00",
    "updated_at": null
  }
]
```

### 3. Update a Template

```bash
# Update a template with new variables
curl -X PUT "http://localhost:8000/api/v1/prompts/1" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello {{ name }}! Welcome to {{ platform }}. Your role is {{ role }}. Your department is {{ department }}.",
    "description": "Updated greeting template with department",
    "meta": {
      "template_variables": ["name", "platform", "role", "department"],
      "author": "test-user",
      "updated": true
    },
    "tags": ["template", "greeting", "updated"]
  }'

# Response:
{
  "id": 1,
  "name": "greeting-template",
  "text": "Hello {{ name }}! Welcome to {{ platform }}. Your role is {{ role }}. Your department is {{ department }}.",
  "description": "Updated greeting template with department",
  "version": 2,
  "meta": {
    "template_variables": ["name", "platform", "role", "department"],
    "author": "test-user",
    "updated": true
  },
  "tags": [
    {"id": 1, "name": "template"},
    {"id": 2, "name": "greeting"},
    {"id": 5, "name": "updated"}
  ],
  "created_at": "2024-03-20T10:00:00",
  "updated_at": "2024-03-20T10:15:00"
}
```

### 4. Delete a Template

```bash
# Delete a template
curl -X DELETE "http://localhost:8000/api/v1/prompts/1"

# Response: 204 No Content
```

### 5. Using Templates in Python

See the complete examples in the [`examples/templating/python`](/examples/templating/python/) directory:

1. Basic string template: `examples/templating/python/string_template_example.py`
2. F-strings: `examples/templating/python/f_strings_example.py`
3. Mako template engine: `examples/templating/python/mako_example.py`
4. Control structures: `examples/templating/python/control_structures_example.py`
5. Jinja2 macros: `examples/templating/python/macro_example.py`

Here's a simple example using Jinja2:

```python
import requests
import jinja2
from jinja2 import Template

# Fetch the prompt template
response = requests.get("http://localhost:8000/api/v1/prompts/1")
prompt_data = response.json()

# Create a Jinja template
template = Template(prompt_data["text"])

# Render with variables
rendered_prompt = template.render(
    name="John",
    platform="Exemplar Prompt Hub",
    role="Developer",
    department="Engineering"
)

print(rendered_prompt)
# Output: Hello John! Welcome to Exemplar Prompt Hub. Your role is Developer. Your department is Engineering.
```

For more advanced examples including control structures, macros, and different template engines, refer to the example files mentioned above. Each example demonstrates different approaches to template rendering:

- `string_template_example.py`: Uses Python's built-in string.Template for simple variable substitution
- `f_strings_example.py`: Shows how to use Python's f-strings for template rendering
- `mako_example.py`: Demonstrates the Mako template engine for high-performance templating
- `control_structures_example.py`: Shows how to use if-else statements and loops in templates
- `macro_example.py`: Demonstrates reusable template components using Jinja2 macros

### 6. Using Templates in JavaScript

See the complete examples in the [`examples/templating/javascript`](/examples/templating/javascript/) directory:

1. Basic template literals: `examples/templating/javascript/template_literals.js`
2. Handlebars.js: `examples/templating/javascript/handlebars_example.js`
3. Mustache.js: `examples/templating/javascript/mustache_example.js`
4. React component: `examples/templating/javascript/react_example.jsx`
5. Control structures: `examples/templating/javascript/control_structures_example.js`
6. Macros/Partials: `examples/templating/javascript/macro_example.js`

Here's a simple example using template literals:

```javascript
// Fetch and render a template
async function renderPrompt(promptId, variables) {
    const response = await fetch(`http://localhost:8000/api/v1/prompts/${promptId}`);
    const promptData = await response.json();
    
    // Create template function
    const template = new Function('variables', `
        with(variables) {
            return \`${promptData.text}\`;
        }
    `);
    
    // Render with variables
    return template(variables);
}

// Usage
const renderedPrompt = await renderPrompt(1, {
    name: 'John',
    platform: 'Exemplar Prompt Hub',
    role: 'Developer',
    department: 'Engineering'
});

console.log(renderedPrompt);
// Output: Hello John! Welcome to Exemplar Prompt Hub. Your role is Developer. Your department is Engineering.
```

For more advanced examples including control structures, macros, and React integration, refer to the example files mentioned above.

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
