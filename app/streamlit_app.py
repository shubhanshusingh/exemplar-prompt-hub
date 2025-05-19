import streamlit as st
import requests
import json

# Set the API URL
API_URL = "http://localhost:8000/api/v1/prompts"

# Function to fetch prompts from the API
def fetch_prompts():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch prompts.")
        return []

# Main function to run the Streamlit app
def main():
    st.title("Exemplar Prompt Hub")
    st.write("Displaying prompts from the database.")

    # Fetch prompts
    prompts = fetch_prompts()

    # Display prompts
    if prompts:
        for prompt in prompts:
            st.write(f"**Name:** {prompt['name']}")
            st.write(f"**Text:** {prompt['text']}")
            st.write(f"**Description:** {prompt['description']}")
            st.write(f"**Version:** {prompt['version']}")
            st.write(f"**Meta:** {json.dumps(prompt['meta'], indent=2)}")
            st.write("---")
    else:
        st.write("No prompts found.")

if __name__ == "__main__":
    main() 