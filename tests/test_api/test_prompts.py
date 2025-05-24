import pytest
import requests
from jinja2 import Template

def test_create_fetch_render_prompt():
    # Create a prompt
    template_data = {
        "name": "test-template",
        "text": "Hello {{name}}! Welcome to {{platform}}.",
        "description": "A test template for API testing.",
        "meta": {
            "template_variables": ["name", "platform"],
            "author": "test-user"
        },
        "tags": ["test", "template"]
    }
    response = requests.post("http://localhost:8000/api/v1/prompts/", json=template_data)
    assert response.status_code == 200
    created_prompt = response.json()
    assert created_prompt["name"] == "test-template"

    # Fetch the prompt
    prompt_id = created_prompt["id"]
    response = requests.get(f"http://localhost:8000/api/v1/prompts/{prompt_id}")
    assert response.status_code == 200
    fetched_prompt = response.json()
    assert fetched_prompt["text"] == "Hello {{name}}! Welcome to {{platform}}."

    # Render the prompt with variables
    variables = {
        "name": "John",
        "platform": "Exemplar Prompt Hub"
    }
    rendered_prompt = Template(fetched_prompt["text"]).render(**variables)
    assert rendered_prompt == "Hello John! Welcome to Exemplar Prompt Hub." 