"""
Example using Mako for prompt templating.
This script creates a prompt, fetches it, and renders it with variables.
"""
import requests
import json
from mako.template import Template

def create_template():
    template_data = {
        "name": "mako-example",
        "text": "Hello ${name}! Welcome to ${platform}. Your role is ${role}. Your department is ${department}.",
        "description": "A template using Mako.",
        "meta": {
            "template_variables": ["name", "platform", "role", "department"],
            "author": "test-user"
        },
        "tags": ["template", "python"]
    }
    response = requests.post("http://localhost:8000/api/v1/prompts/", json=template_data)
    response.raise_for_status()
    return response.json()

def fetch_prompt(prompt_id):
    response = requests.get(f"http://localhost:8000/api/v1/prompts/{prompt_id}")
    response.raise_for_status()
    return response.json()

def render_prompt(template, variables):
    return Template(template).render(**variables)

def main():
    try:
        # Create the template
        created_prompt = create_template()
        print("Created prompt:", json.dumps(created_prompt, indent=2))
        # Fetch the prompt
        prompt_data = fetch_prompt(created_prompt["id"])
        # Example variables
        variables = {
            "name": "John",
            "platform": "Exemplar Prompt Hub",
            "role": "Developer",
            "department": "Engineering"
        }
        # Render the prompt
        rendered_prompt = render_prompt(prompt_data["text"], variables)
        print("\nRendered prompt:")
        print(rendered_prompt)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main() 