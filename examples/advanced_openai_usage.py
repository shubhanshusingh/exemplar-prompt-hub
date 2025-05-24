import asyncio
import os
import requests
from openai import AsyncOpenAI

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def use_prompt_api():
    # Example 1: Code Review
    # First, create the prompt via API
    code_review_prompt = {
        "name": "code-review-assistant",
        "text": """Please review the following code and provide feedback on:
1. Code quality and best practices
2. Potential bugs or issues
3. Performance considerations
4. Security concerns
5. Suggestions for improvement

Code to review:
{code}

Please provide a detailed review with specific examples and suggestions.""",
        "description": "AI-powered code review assistant",
        "tags": ["code-review", "development", "best-practices"],
        "meta": {
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 1000
        }
    }
    
    # Create prompt via API
    response = requests.post("http://localhost:8000/api/v1/prompts/", json=code_review_prompt)
    created_prompt = response.json()
    print("\nCreated code review prompt:", created_prompt['id'])

    # Example code to review
    sample_code = """
def calculate_factorial(n):
    if n < 0:
        return None
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
    """

    # Fetch the prompt template
    prompt_response = requests.get(f"http://localhost:8000/api/v1/prompts/{created_prompt['id']}")
    prompt_data = prompt_response.json()

    # Use the prompt with OpenAI
    response = await client.chat.completions.create(
        model=prompt_data['meta']['model'],
        messages=[
            {"role": "system", "content": "You are a code review expert."},
            {"role": "user", "content": prompt_data['text'].format(code=sample_code)}
        ],
        temperature=prompt_data['meta']['temperature'],
        max_tokens=prompt_data['meta']['max_tokens']
    )
    print("\nCode Review Response:")
    print(response.choices[0].message.content)

    # Example 2: Text Summarization
    summary_prompt = {
        "name": "text-summarizer",
        "text": """Please summarize the following text in a concise and informative way.
Focus on the main points and key takeaways.

Text to summarize:
{text}

Please provide a summary that is approximately {length} words long.""",
        "description": "AI-powered text summarization",
        "tags": ["summarization", "text-processing"],
        "meta": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.3,
            "max_tokens": 500
        }
    }

    # Create prompt via API
    response = requests.post("http://localhost:8000/api/v1/prompts/", json=summary_prompt)
    created_summary_prompt = response.json()
    print("\nCreated summary prompt:", created_summary_prompt['id'])

    # Example text to summarize
    sample_text = """
    Artificial Intelligence (AI) is transforming the way we live and work. 
    From virtual assistants to self-driving cars, AI technologies are becoming 
    increasingly integrated into our daily lives. Machine learning, a subset of AI, 
    enables computers to learn from data and improve their performance over time. 
    Deep learning, a more advanced form of machine learning, uses neural networks 
    to process complex patterns and make decisions. These technologies are being 
    applied across various industries, including healthcare, finance, and 
    transportation, leading to improved efficiency and new capabilities.
    """

    # Fetch the prompt template
    prompt_response = requests.get(f"http://localhost:8000/api/v1/prompts/{created_summary_prompt['id']}")
    prompt_data = prompt_response.json()

    # Use the summary prompt with OpenAI
    response = await client.chat.completions.create(
        model=prompt_data['meta']['model'],
        messages=[
            {"role": "system", "content": "You are a text summarization expert."},
            {"role": "user", "content": prompt_data['text'].format(
                text=sample_text,
                length=50
            )}
        ],
        temperature=prompt_data['meta']['temperature'],
        max_tokens=prompt_data['meta']['max_tokens']
    )
    print("\nSummary Response:")
    print(response.choices[0].message.content)

    # Example 3: Creative Writing
    creative_prompt = {
        "name": "creative-story-generator",
        "text": """Write a short story based on the following elements:
Genre: {genre}
Theme: {theme}
Main character: {character}
Setting: {setting}

Please create an engaging story that incorporates these elements.""",
        "description": "AI-powered creative writing assistant",
        "tags": ["creative-writing", "storytelling"],
        "meta": {
            "model": "gpt-4",
            "temperature": 0.9,
            "max_tokens": 1500
        }
    }

    # Create prompt via API
    response = requests.post("http://localhost:8000/api/v1/prompts/", json=creative_prompt)
    created_story_prompt = response.json()
    print("\nCreated story prompt:", created_story_prompt['id'])

    # Fetch the prompt template
    prompt_response = requests.get(f"http://localhost:8000/api/v1/prompts/{created_story_prompt['id']}")
    prompt_data = prompt_response.json()

    # Use the creative writing prompt with OpenAI
    response = await client.chat.completions.create(
        model=prompt_data['meta']['model'],
        messages=[
            {"role": "system", "content": "You are a creative writing expert."},
            {"role": "user", "content": prompt_data['text'].format(
                genre="science fiction",
                theme="exploration",
                character="a space archaeologist",
                setting="an ancient alien city on Mars"
            )}
        ],
        temperature=prompt_data['meta']['temperature'],
        max_tokens=prompt_data['meta']['max_tokens']
    )
    print("\nCreative Writing Response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(use_prompt_api()) 