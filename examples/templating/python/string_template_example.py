"""
Example using Python's built-in string.Template for prompt templating.
"""
from string import Template
import requests
import json
from typing import Dict, Any

def fetch_prompt(prompt_id: str) -> Dict[str, Any]:
    """Fetch a prompt from the API."""
    response = requests.get(f"http://localhost:8000/api/v1/prompts/{prompt_id}")
    response.raise_for_status()
    return response.json()

def render_prompt(template: str, variables: Dict[str, str]) -> str:
    """Render a template with variables using string.Template."""
    return Template(template).substitute(variables)

def main():
    # Example prompt ID (replace with actual ID)
    prompt_id = "example-prompt-id"
    
    try:
        # Fetch the prompt
        prompt_data = fetch_prompt(prompt_id)
        print(f"Fetched prompt: {json.dumps(prompt_data, indent=2)}")
        
        # Variables for template
        variables = {
            "name": "John",
            "platform": "Exemplar Prompt Hub",
            "role": "Developer"
        }
        
        # Render the prompt
        rendered_prompt = render_prompt(prompt_data["text"], variables)
        print("\nRendered prompt:")
        print(rendered_prompt)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching prompt: {e}")
    except KeyError as e:
        print(f"Error accessing prompt data: {e}")
    except ValueError as e:
        print(f"Error rendering template: {e}")

if __name__ == "__main__":
    main() 