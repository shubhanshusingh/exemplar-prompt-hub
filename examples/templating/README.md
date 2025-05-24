# Prompt Templating Examples

This directory contains examples of different templating approaches for rendering prompts from the Exemplar Prompt Hub API.

## Python Examples

### Prerequisites
```bash
pip install requests mako jinja2
```

### Available Examples
1. `python/string_template_example.py` - Using Python's built-in string.Template
2. `python/f_strings_example.py` - Using Python's f-strings
3. `python/mako_example.py` - Using Mako template engine
4. `python/control_structures_example.py` - Using control structures (if-else, loops)
5. `python/macro_example.py` - Using Jinja2 macros

### Running Python Examples
```bash
# Replace example-prompt-id with actual prompt ID
python python/string_template_example.py
python python/f_strings_example.py
python python/mako_example.py
python python/control_structures_example.py
python python/macro_example.py
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
5. `javascript/control_structures_example.js` - Using control structures with Handlebars
6. `javascript/macro_example.js` - Using Handlebars partials (macros)

### Running JavaScript Examples
```bash
# Using Node.js
node javascript/template_literals.js
node javascript/handlebars_example.js
node javascript/mustache_example.js
node javascript/control_structures_example.js
node javascript/macro_example.js

# For React example, you'll need to set up a React project
# and import the component
```

## Advanced Features

### Control Structures
Examples demonstrating:
- Conditional rendering (if-else)
- Loops (for-each)
- Nested templates
- Variable comparison

### Macros/Partials
Examples demonstrating:
- Reusable template components
- Template inheritance
- Custom helpers/filters
- Nested macros

## Comparison of Approaches

### Python
- `string.Template`: Simple, built-in, limited features
- `f-strings`: Modern, readable, but less flexible
- `Mako`: Fast, flexible, good for large templates
- `Jinja2`: Full-featured, powerful, widely used

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
5. Control structures
6. Macros/partials

## Notes

- Replace `example-prompt-id` with actual prompt IDs from your API
- Ensure the API server is running at `http://localhost:8000`
- Check the API documentation for available endpoints and response formats
- For JavaScript examples, ensure you have Node.js installed
- For React example, set up a React project with proper dependencies 