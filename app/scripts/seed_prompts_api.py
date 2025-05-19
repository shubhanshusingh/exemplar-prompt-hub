import requests

def seed_prompts_api():
    base_url = "http://localhost:8000/api/v1"
    
    # Create prompts
    prompt1 = {
        "name": "AI Prompt 1",
        "text": "This is a sample AI prompt.",
        "version": 1,
        "description": "A sample prompt for AI applications.",
        "meta": {},
        "tags": ["AI"]
    }
    prompt2 = {
        "name": "ML Prompt 1",
        "text": "This is a sample Machine Learning prompt.",
        "version": 1,
        "description": "A sample prompt for ML applications.",
        "meta": {},
        "tags": ["Machine Learning"]
    }
    
    response1 = requests.post(f"{base_url}/prompts/", json=prompt1)
    response2 = requests.post(f"{base_url}/prompts/", json=prompt2)
    
    if response1.status_code == 200 and response2.status_code == 200:
        print("Prompts seeded successfully!")
    else:
        print(f"Error seeding prompts. Status code: {response1.status_code}, {response2.status_code}")
        print(f"Response 1: {response1.text}")
        print(f"Response 2: {response2.text}")

if __name__ == "__main__":
    seed_prompts_api() 