"""
Example: Using a prompt from Exemplar Prompt Hub with Haystack
"""
import requests
from haystack.nodes import PromptNode
from haystack.utils import print_answers
import os

# Fetch the prompt from the API
PROMPT_ID = 1  # Change as needed
def fetch_prompt(prompt_id):
    response = requests.get(f"http://localhost:8000/api/v1/prompts/{prompt_id}")
    response.raise_for_status()
    return response.json()

def main():
    prompt_data = fetch_prompt(PROMPT_ID)
    print("Fetched prompt:", prompt_data["text"])

    # Prepare variables for the prompt
    variables = {
        "name": "John",
        "platform": "Exemplar Prompt Hub",
        "role": "Developer"
    }
    prompt_str = prompt_data["text"].format(**variables)
    print("\nRendered prompt:")
    print(prompt_str)

    # Use Haystack PromptNode (OpenAI backend)
    openai_api_key = os.getenv("OPENAI_API_KEY")
    node = PromptNode("gpt-3.5-turbo", api_key=openai_api_key, model_kwargs={"temperature": 0})
    result = node(prompt_str)
    print("\nHaystack LLM Response:")
    print(result)

if __name__ == "__main__":
    main() 