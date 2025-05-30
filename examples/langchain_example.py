"""
Example: Using a prompt from Exemplar Prompt Hub with LangChain
"""
import requests
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
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

    # Create a LangChain PromptTemplate
    template = PromptTemplate(
        input_variables=list(variables.keys()),
        template=prompt_data["text"]
    )
    prompt_str = template.format(**variables)
    print("\nRendered prompt:")
    print(prompt_str)

    # Use OpenAI LLM (requires OPENAI_API_KEY env var)
    llm = OpenAI(temperature=0)
    result = llm(prompt_str)
    print("\nLLM Response:")
    print(result)

if __name__ == "__main__":
    main() 