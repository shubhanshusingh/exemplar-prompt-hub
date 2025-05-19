# 🚀 Exemplar Prompt Hub

A modern REST API service for managing and serving AI prompts. This service provides a centralized repository for storing, versioning, and retrieving prompts for various AI applications. It uses PostgreSQL as the database for robust and scalable data management.

## ✨ Features

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
Contributions are welcome! Please feel free to submit a Pull Request. For detailed contribution guidelines, please refer to the [CONTRIBUTION.md](CONTRIBUTION.md) file.

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
   - If you provide a new version number, the system will create a new entry in the `PromptVersions` table.
   - If you do not provide a version number, the system will increment the existing version number by 1.

### Example Update Request
```json
{
  "name": "Updated Prompt Name",
  "text": "Updated prompt text",
  "description": "Updated description",
  "version": 2,
  "meta": {"key": "value"}
}
```

### Note
Ensure that the prompt you are updating exists in the database before attempting to update it.

## 🌟 Streamlit UI

The project includes a Streamlit UI application that allows you to view prompts stored in the database. This UI provides a user-friendly interface to display prompt details such as name, text, description, version, and metadata.

### Running the Streamlit App

1. **Ensure the API is Running:**
   Make sure your FastAPI application is running so that the Streamlit app can fetch prompts from the API.

2. **Run the Streamlit App:**
   Use the following command to start the Streamlit app:
   ```bash
   streamlit run app/streamlit_app.py
   ```

3. **Access the UI:**
   Open your web browser and go to `http://localhost:8501` to view the Streamlit UI.

### Features of the Streamlit UI
- Displays a list of prompts fetched from the API.
- Shows details for each prompt, including name, text, description, version, and metadata.
- Provides a clean and intuitive interface for users to interact with the prompt data.

### Note
Ensure that the API is accessible at `http://localhost:8000/api/v1/prompts` for the Streamlit app to function correctly. 