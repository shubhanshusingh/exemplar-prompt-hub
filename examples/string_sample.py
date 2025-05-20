from string import Template
import requests
import re

# Fetch the prompt
response = requests.get("http://localhost:8000/api/v1/prompts/?skip=0&limit=1&search=greeting-template")
prompt_data = response.json()

# Convert Jinja2 variables to Python string.Template format
# From: {{ variable }} to: ${variable}
template_text = re.sub(r'{{ (.*?) }}', r'${\1}', prompt_data[0]["text"])
print("Original template:", prompt_data[0]["text"])
print("Converted template:", template_text)

# Create template
template = Template(template_text)

# Render with variables
rendered_prompt = template.substitute(
    name="John",
    platform="Exemplar Prompt Hub",
    role="Developer"
)

print("Rendered output:", rendered_prompt)