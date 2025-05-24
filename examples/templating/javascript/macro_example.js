/**
 * Example using macros in prompt templating.
 */
import Handlebars from 'handlebars';

async function createMacroTemplate() {
    const templateData = {
        name: "macro-template",
        text: `{{#*inline "formatItem"}}
- {{titleCase this}}
{{/inline}}

{{#each categories}}{{this.name}}:
{{#each this.items}}{{> formatItem}}{{/each}}
{{/each}}`,
        description: "Template using Handlebars partials (macros)",
        meta: {
            template_variables: ["categories"],
            author: "test-user"
        },
        tags: ["template", "macro"]
    };
    
    const response = await fetch("http://localhost:8000/api/v1/prompts/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(templateData)
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
}

async function renderPrompt(template, variables) {
    // Register helper for title case
    Handlebars.registerHelper('titleCase', function(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    });
    
    // Compile template
    const compiledTemplate = Handlebars.compile(template);
    
    // Render with variables
    return compiledTemplate(variables);
}

async function main() {
    try {
        // Create the template
        const templateData = await createMacroTemplate();
        console.log('Created template:', JSON.stringify(templateData, null, 2));
        
        // Example data with categories and items
        const variables = {
            categories: [
                {
                    name: "Frontend",
                    items: ["react", "vue", "angular"]
                },
                {
                    name: "Backend",
                    items: ["python", "node", "java"]
                },
                {
                    name: "Database",
                    items: ["postgres", "mongodb", "redis"]
                }
            ]
        };
        
        // Render the prompt
        const renderedPrompt = await renderPrompt(templateData.text, variables);
        console.log('\nRendered prompt:');
        console.log(renderedPrompt);
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main().catch(console.error); 