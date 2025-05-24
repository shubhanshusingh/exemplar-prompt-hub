import requests
import jinja2
from jinja2 import Template
from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Create a prompt


# curl -X POST "http://localhost:8000/api/v1/prompts/" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "name": "greeting-template",
#     "text": "Hello {{ name }}! Welcome to {{ platform }}. Your role is {{ role }}.",
#     "description": "A greeting template with dynamic variables",
#     "meta": {
#       "template_variables": ["name", "platform", "role"],
#       "author": "test-user"
#     },
#     "tags": ["template", "greeting"]
#   }'

# Fetch the prompt template
response = requests.get("http://localhost:8000/api/v1/prompts/?skip=0&limit=1&search=greeting-template")
prompt_data = response.json()

# Create a Jinja template
template = Template(prompt_data[0]["text"])

# Render with variables
rendered_prompt = template.render(
    name="John",
    platform="Exemplar Prompt Hub",
    role="Developer",
    department="Engineering"
)
print("\nRendered Prompt:")
print(rendered_prompt)
# Use the new OpenAI client format
completion = client.chat.completions.create(
    model="o1-mini",
    messages=[
        {
            "role": "user",
            "content": rendered_prompt
        }
    ]
)

print("\nGenerated Response:")
print(completion.choices[0].message.content)
