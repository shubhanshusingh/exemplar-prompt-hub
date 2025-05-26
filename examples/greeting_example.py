"""
Example demonstrating the creation, update, and usage of a greeting template.
"""
import requests
import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_greeting_template() -> Dict[str, Any]:
    """Create the initial greeting template."""
    template_data = {
        "name": "greeting-template",
        "text": "Hello {{ name }}! Welcome to {{ platform }}. Your role is {{ role }}.",
        "description": "A greeting template with dynamic variables",
        "meta": {
            "template_variables": ["name", "platform", "role"],
            "author": "test-user"
        },
        "tags": ["template", "greeting"]
    }
    
    logger.info("Creating greeting template with data: %s", json.dumps(template_data, indent=2))
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/prompts/",
            json=template_data
        )
        response.raise_for_status()
        result = response.json()
        logger.info("Successfully created template with ID: %s", result.get("id"))
        return result
    except requests.exceptions.RequestException as e:
        logger.error("Failed to create template: %s", str(e))
        if hasattr(e.response, 'text'):
            logger.error("Response content: %s", e.response.text)
        raise

def update_greeting_template(prompt_id: int) -> Dict[str, Any]:
    """Update the greeting template to include department."""
    update_data = {
        "text": "Hello {{ name }}! Welcome to {{ platform }}. Your role is {{ role }}. Your department is {{ department }}.",
        "description": "Updated greeting template with department",
        "meta": {
            "template_variables": ["name", "platform", "role", "department"],
            "author": "test-user",
            "updated": True
        },
        "tags": ["template", "greeting", "updated"]
    }
    
    logger.info("Updating template %s with data: %s", prompt_id, json.dumps(update_data, indent=2))
    
    try:
        response = requests.put(
            f"http://localhost:8000/api/v1/prompts/{prompt_id}",
            json=update_data
        )
        response.raise_for_status()
        result = response.json()
        logger.info("Successfully updated template to version: %s", result.get("version"))
        return result
    except requests.exceptions.RequestException as e:
        logger.error("Failed to update template: %s", str(e))
        if hasattr(e.response, 'text'):
            logger.error("Response content: %s", e.response.text)
        raise

def use_greeting_template(prompt_id: int, version: int = None) -> Dict[str, Any]:
    """Use the greeting template in the playground."""
    playground_data = {
        "prompt_id": prompt_id,
        "models": ["openai/gpt-4", "anthropic/claude-3-opus"],
        "variables": {
            "name": "John",
            "platform": "Exemplar Prompt Hub",
            "role": "Developer",
            "department": "Engineering"
        }
    }
    
    if version is not None:
        playground_data["version"] = version
        logger.info("Using specific version %s of template %s", version, prompt_id)
    else:
        logger.info("Using latest version of template %s", prompt_id)
    
    logger.info("Sending playground request with data: %s", json.dumps(playground_data, indent=2))
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/prompts/playground",
            json=playground_data
        )
        response.raise_for_status()
        result = response.json()
        logger.info("Successfully got playground response with %d models", len(result.get("responses", {})))
        return result
    except requests.exceptions.RequestException as e:
        logger.error("Failed to use template in playground: %s", str(e))
        if hasattr(e.response, 'text'):
            logger.error("Response content: %s", e.response.text)
        raise

def main():
    try:
        # Create the initial template
        logger.info("Starting template creation process...")
        template = create_greeting_template()
        print("\n1. Created greeting template:")
        print(json.dumps(template, indent=2))
        
        # Update the template
        logger.info("Starting template update process...")
        updated_template = update_greeting_template(template["id"])
        print("\n2. Updated greeting template:")
        print(json.dumps(updated_template, indent=2))
        
        # Use the template with latest version
        logger.info("Testing template with latest version...")
        playground_response = use_greeting_template(template["id"])
        print("\n3. Playground response (latest version):")
        print(json.dumps(playground_response, indent=2))
        
        # Use the template with version 1
        logger.info("Testing template with version 1...")
        playground_response_v1 = use_greeting_template(template["id"], version=1)
        print("\n4. Playground response (version 1):")
        print(json.dumps(playground_response_v1, indent=2))
        
    except requests.exceptions.RequestException as e:
        logger.error("Error with API request: %s", str(e))
        if hasattr(e.response, 'text'):
            logger.error("Response content: %s", e.response.text)
    except Exception as e:
        logger.error("Unexpected error: %s", str(e), exc_info=True)

if __name__ == "__main__":
    main()
