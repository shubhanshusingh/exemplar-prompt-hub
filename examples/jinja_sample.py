import requests
import jinja2
from jinja2 import Template

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

print(rendered_prompt)