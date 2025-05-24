# Prompt Templating Examples

This directory contains examples of different templating approaches for rendering prompts from the Exemplar Prompt Hub API.

## Python Examples

### Prerequisites
```bash
pip install requests mako
```

### Available Examples
1. `python/string_template_example.py` - Using Python's built-in string.Template
2. `python/f_strings_example.py` - Using Python's f-strings
3. `python/mako_example.py` - Using Mako template engine

### Running Python Examples
```bash
# Replace example-prompt-id with actual prompt ID
python python/string_template_example.py
python python/f_strings_example.py
python python/mako_example.py
```

## JavaScript Examples

### Prerequisites
```bash
npm install handlebars mustache
```

### Available Examples
1. `javascript/template_literals.js` - Using JavaScript template literals
2. `javascript/handlebars_example.js` - Using Handlebars.js
3. `javascript/mustache_example.js` - Using Mustache.js
4. `javascript/react_example.jsx` - Using React with template strings

### Running JavaScript Examples
```bash
# Using Node.js
node javascript/template_literals.js
node javascript/handlebars_example.js
node javascript/mustache_example.js

# For React example, you'll need to set up a React project
# and import the component
```

## Comparison of Approaches

### Python
- `string.Template`: Simple, built-in, limited features
- `f-strings`: Modern, readable, but less flexible
- `Mako`: Fast, flexible, good for large templates

### JavaScript
- Template Literals: Native, simple, limited features
- Handlebars.js: Powerful, extensible, good for complex templates
- Mustache.js: Logic-less, simple, good for basic needs
- React: Component-based, good for UI integration

## Choosing the Right Approach

- For simple templates: Use built-in solutions (string.Template, f-strings, Template Literals)
- For complex templates: Use full-featured engines (Jinja2, Handlebars.js)
- For UI integration: Use framework-specific solutions (React)
- For performance: Consider Mako or Mustache.js

## Common Features

All examples demonstrate:
1. Fetching prompts from the API
2. Error handling
3. Template rendering
4. Variable substitution

## Notes

- Replace `example-prompt-id` with actual prompt IDs from your API
- Ensure the API server is running at `http://localhost:8000`
- Check the API documentation for available endpoints and response formats 