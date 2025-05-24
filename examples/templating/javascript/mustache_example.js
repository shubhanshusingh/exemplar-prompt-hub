/**
 * Example using Mustache.js for prompt templating.
 */
import Mustache from 'mustache';

async function fetchPrompt(promptId) {
    const response = await fetch(`http://localhost:8000/api/v1/prompts/${promptId}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

async function renderPrompt(promptId, variables) {
    try {
        // Fetch the prompt
        const promptData = await fetchPrompt(promptId);
        console.log('Fetched prompt:', JSON.stringify(promptData, null, 2));
        
        // Render with variables
        const renderedPrompt = Mustache.render(promptData.text, variables);
        console.log('\nRendered prompt:');
        console.log(renderedPrompt);
        
        return renderedPrompt;
    } catch (error) {
        console.error('Error:', error.message);
        throw error;
    }
}

// Example usage
const variables = {
    name: 'John',
    platform: 'Exemplar Prompt Hub',
    role: 'Developer'
};

// Replace with actual prompt ID
const promptId = 'example-prompt-id';

renderPrompt(promptId, variables)
    .catch(error => console.error('Failed to render prompt:', error)); 