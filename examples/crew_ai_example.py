"""
Example: Using a prompt from Exemplar Prompt Hub with CrewAI
"""
import requests
import os
# CrewAI is a multi-agent framework. We'll show how to use a prompt as a task for an agent.
try:
    from crewai import Agent, Task, Crew
except ImportError:
    print("Please install crewai: pip install crewai")
    exit(1)

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

    # Define a CrewAI agent and task
    agent = Agent(
        name="Coding Assistant",
        role="Expert Developer",
        goal="Help users with coding tasks and best practices."
    )
    task = Task(
        description=prompt_str,
        expected_output="A helpful, well-documented code solution."
    )
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.run()
    print("\nCrewAI Response:")
    print(result)

if __name__ == "__main__":
    main() 