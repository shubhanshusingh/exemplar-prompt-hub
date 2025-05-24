/**
 * Example using control structures (if-else, loops) in prompt templating.
 */
import Handlebars from 'handlebars';

async function createControlTemplate() {
    const templateData = {
        name: "advanced-template",
        text: `{{#if (eq user_type "admin")}}Welcome, Administrator!{{else}}Welcome, User!{{/if}}

{{#each features}}- {{this}}
{{/each}}`,
        description: "Advanced template with control structures",
        meta: {
            template_variables: ["user_type", "features"],
            author: "test-user"
        },
        tags: ["template", "advanced"]
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
    // Register helper for equality comparison
    Handlebars.registerHelper('eq', function(a, b) {
        return a === b;
    });
    
    // Compile template
    const compiledTemplate = Handlebars.compile(template);
    
    // Render with variables
    return compiledTemplate(variables);
}

async function main() {
    try {
        // Create the template
        const templateData = await createControlTemplate();
        console.log('Created template:', JSON.stringify(templateData, null, 2));
        
        // Example 1: Admin user
        const adminVariables = {
            user_type: "admin",
            features: ["Dashboard", "User Management", "Settings"]
        };
        const adminPrompt = await renderPrompt(templateData.text, adminVariables);
        console.log('\nAdmin prompt:');
        console.log(adminPrompt);
        
        // Example 2: Regular user
        const userVariables = {
            user_type: "user",
            features: ["Profile", "Messages", "Notifications"]
        };
        const userPrompt = await renderPrompt(templateData.text, userVariables);
        console.log('\nUser prompt:');
        console.log(userPrompt);
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main().catch(console.error); 