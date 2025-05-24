"""
Example using macros in prompt templating.
"""
import requests
import json
from typing import Dict, Any, List

def fetch_prompt(prompt_id: str) -> Dict[str, Any]:
    """Fetch a prompt from the API."""
    response = requests.get(f"http://localhost:8000/api/v1/prompts/{prompt_id}")
    response.raise_for_status()
    return response.json()

def create_macro_template() -> Dict[str, Any]:
    """Create a template with macros."""
    template_data = {
        "name": "macro-template",
        "text": """{% macro format_item(item) %}- {{ item|title }}
{% endmacro %}

{% for category in categories %}{{ category.name }}:
{% for item in category.items %}{{ format_item(item) }}{% endfor %}
{% endfor %}""",
        "description": "Template using Jinja2 macros",
        "meta": {
            "template_variables": ["categories"],
            "author": "test-user"
        },
        "tags": ["template", "macro"]
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
        template_data = create_macro_template()
        print(f"Created template: {json.dumps(template_data, indent=2)}")
        
        # Example data with categories and items
        variables = {
            "categories": [
                {
                    "name": "Frontend",
                    "items": ["react", "vue", "angular"]
                },
                {
                    "name": "Backend",
                    "items": ["python", "node", "java"]
                },
                {
                    "name": "Database",
                    "items": ["postgres", "mongodb", "redis"]
                }
            ]
        }
        
        # Render the prompt
        rendered_prompt = render_prompt(template_data["text"], variables)
        print("\nRendered prompt:")
        print(rendered_prompt)
        
    except requests.exceptions.RequestException as e:
        print(f"Error with API request: {e}")
    except Exception as e:
        print(f"Error rendering template: {e}")

if __name__ == "__main__":
    main() 