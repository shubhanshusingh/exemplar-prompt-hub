/**
 * Example using JavaScript template literals for prompt templating.
 * This script creates a prompt, fetches it, and renders it with variables.
 */
async function createTemplate() {
    const templateData = {
        name: "template-literals-example",
        text: "Hello ${name}! Welcome to ${platform}. Your role is ${role}. Your department is ${department}.",
        description: "A template using JavaScript template literals.",
        meta: {
            template_variables: ["name", "platform", "role", "department"],
            author: "test-user"
        },
        tags: ["template", "javascript"]
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

async function fetchPrompt(promptId) {
    const response = await fetch(`http://localhost:8000/api/v1/prompts/${promptId}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

async function renderPrompt(template, variables) {
    // Create template function
    const templateFn = new Function('variables', `with(variables) { return \`${template}\`; }`);
    return templateFn(variables);
}

async function main() {
    try {
        // Create the template
        const createdPrompt = await createTemplate();
        console.log('Created prompt:', JSON.stringify(createdPrompt, null, 2));
        // Fetch the prompt
        const promptData = await fetchPrompt(createdPrompt.id);
        // Example variables
        const variables = {
            name: 'John',
            platform: 'Exemplar Prompt Hub',
            role: 'Developer',
            department: 'Engineering'
        };
        // Render the prompt
        const renderedPrompt = await renderPrompt(promptData.text, variables);
        console.log('\nRendered prompt:');
        console.log(renderedPrompt);
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main().catch(console.error); 