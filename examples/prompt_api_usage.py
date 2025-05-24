import asyncio
import requests
from openai import AsyncOpenAI
import os

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def main():
    # Example 1: Create a new prompt
    new_prompt = {
        "name": "Customer Support Response",
        "text": "Thank you for contacting our support team. We appreciate your patience.",
        "description": "Standard response for customer support inquiries",
        "tags": ["support", "customer-service"],
        "meta": {
            "category": "support",
            "priority": "high"
        }
    }
    
    # Create prompt via API
    response = requests.post("http://localhost:8000/api/v1/prompts/", json=new_prompt)
    created_prompt = response.json()
    print("\n1. Created new prompt:")
    print(f"ID: {created_prompt['id']}")
    print(f"Name: {created_prompt['name']}")
    print(f"Tags: {[tag['name'] for tag in created_prompt['tags']]}")

    # Example 2: Get a prompt by ID
    prompt_id = created_prompt['id']
    response = requests.get(f"http://localhost:8000/api/v1/prompts/{prompt_id}")
    retrieved_prompt = response.json()
    print("\n2. Retrieved prompt:")
    print(f"Name: {retrieved_prompt['name']}")
    print(f"Description: {retrieved_prompt['description']}")
    print(f"Version: {retrieved_prompt['version']}")

    # Example 3: Update a prompt
    update_data = {
        "text": "Thank you for contacting our support team. We appreciate your patience and will get back to you shortly.",
        "description": "Updated standard response for customer support inquiries",
        "tags": ["support", "customer-service", "priority"],
        "meta": {
            "category": "support",
            "priority": "high",
            "response_time": "24h"
        }
    }
    response = requests.put(f"http://localhost:8000/api/v1/prompts/{prompt_id}", json=update_data)
    updated_prompt = response.json()
    print("\n3. Updated prompt:")
    print(f"New text: {updated_prompt['text']}")
    print(f"New tags: {[tag['name'] for tag in updated_prompt['tags']]}")
    print(f"Version history: {len(updated_prompt['versions'])} versions")

    # Example 4: Search prompts
    response = requests.get("http://localhost:8000/api/v1/prompts/?search=support")
    search_results = response.json()
    print("\n4. Search results for 'support':")
    for prompt in search_results:
        print(f"- {prompt['name']} (ID: {prompt['id']})")

    # Example 5: List all prompts
    response = requests.get("http://localhost:8000/api/v1/prompts/?limit=5")
    all_prompts = response.json()
    print("\n5. List of prompts (limited to 5):")
    for prompt in all_prompts:
        print(f"- {prompt['name']} (ID: {prompt['id']})")

    # Example 6: Delete a prompt
    response = requests.delete(f"http://localhost:8000/api/v1/prompts/{prompt_id}")
    delete_result = response.status_code == 200
    print(f"\n6. Deleted prompt: {delete_result}")

if __name__ == "__main__":
    asyncio.run(main()) 