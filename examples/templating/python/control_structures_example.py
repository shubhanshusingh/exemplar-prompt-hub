"""
Example using control structures (if-else, loops) in prompt templating.
"""
import requests
import json
from typing import Dict, Any, List

def fetch_prompt(prompt_id: str) -> Dict[str, Any]:
    """Fetch a prompt from the API."""
    response = requests.get(f"http://localhost:8000/api/v1/prompts/{prompt_id}")
    response.raise_for_status()
    return response.json()

def create_control_template() -> Dict[str, Any]:
    """Create a template with control structures."""
    template_data = {
        "name": "advanced-template",
        "text": """{% if user_type == "admin" %}Welcome, Administrator!{% else %}Welcome, User!{% endif %}

{% for item in features %}- {{ item }}
{% endfor %}""",
        "description": "Advanced template with control structures",
        "meta": {
            "template_variables": ["user_type", "features"],
            "author": "test-user"
        },
        "tags": ["template", "advanced"]
    }
    
    response = requests.post(
        "http://localhost:8000/api/v1/prompts/",
        json=template_data
    )
    response.raise_for_status()
    return response.json()

def render_prompt(template: str, variables: Dict[str, Any]) -> str:
    """Render a template with variables using Jinja2."""
    from jinja2 import Template
    return Template(template).render(**variables)

def main():
    try:
        # Create the template
        template_data = create_control_template()
        print(f"Created template: {json.dumps(template_data, indent=2)}")
        
        # Example 1: Admin user
        admin_variables = {
            "user_type": "admin",
            "features": ["Dashboard", "User Management", "Settings"]
        }
        admin_prompt = render_prompt(template_data["text"], admin_variables)
        print("\nAdmin prompt:")
        print(admin_prompt)
        
        # Example 2: Regular user
        user_variables = {
            "user_type": "user",
            "features": ["Profile", "Messages", "Notifications"]
        }
        user_prompt = render_prompt(template_data["text"], user_variables)
        print("\nUser prompt:")
        print(user_prompt)
        
    except requests.exceptions.RequestException as e:
        print(f"Error with API request: {e}")
    except Exception as e:
        print(f"Error rendering template: {e}")

if __name__ == "__main__":
    main() 