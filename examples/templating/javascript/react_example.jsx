/**
 * Example using React with template strings for prompt templating.
 */
import React, { useState, useEffect } from 'react';

function PromptRenderer({ promptId, variables }) {
    const [prompt, setPrompt] = useState('');
    const [renderedPrompt, setRenderedPrompt] = useState('');
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchPrompt() {
            try {
                const response = await fetch(`http://localhost:8000/api/v1/prompts/${promptId}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const promptData = await response.json();
                setPrompt(promptData.text);
            } catch (error) {
                setError(error.message);
            }
        }
        fetchPrompt();
    }, [promptId]);

    useEffect(() => {
        if (prompt) {
            try {
                const template = new Function('variables', `
                    with(variables) {
                        return \`${prompt}\`;
                    }
                `);
                setRenderedPrompt(template(variables));
            } catch (error) {
                setError(error.message);
            }
        }
    }, [prompt, variables]);

    if (error) {
        return <div className="error">Error: {error}</div>;
    }

    return <div className="prompt">{renderedPrompt}</div>;
}

// Example usage
function App() {
    const variables = {
        name: 'John',
        platform: 'Exemplar Prompt Hub',
        role: 'Developer'
    };

    // Replace with actual prompt ID
    const promptId = 'example-prompt-id';

    return (
        <div className="app">
            <h1>Prompt Renderer</h1>
            <PromptRenderer 
                promptId={promptId}
                variables={variables}
            />
        </div>
    );
}

export default App; 