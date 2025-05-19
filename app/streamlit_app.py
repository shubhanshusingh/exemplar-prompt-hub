import streamlit as st
import requests
import json
from datetime import datetime

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

# Function to add a new prompt
def add_prompt(name, text, description, meta, tags):
    prompt_data = {
        "name": name,
        "text": text,
        "description": description,
        "version": 1,  # Always start with version 1 (integer)
        "meta": meta,
        "tags": tags
    }
    response = requests.post(API_URL, json=prompt_data)
    if response.status_code == 200:
        st.success("Prompt added successfully!")
    else:
        st.error(f"Failed to add prompt: {response.text}")

# Function to delete a prompt
def delete_prompt(prompt_id):
    response = requests.delete(f"{API_URL}/{prompt_id}")
    if response.status_code == 200:
        st.success("Prompt deleted successfully!")
    else:
        st.error(f"Failed to delete prompt: {response.text}")

# Function to update a prompt
def update_prompt(prompt_id, text, description, meta, tags):
    prompt_data = {
        "text": text,
        "description": description,
        "meta": meta,
        "tags": tags
    }
    response = requests.put(f"{API_URL}/{prompt_id}", json=prompt_data)
    if response.status_code == 200:
        st.success("Prompt updated successfully!")
    else:
        st.error(f"Failed to update prompt: {response.text}")

# Function to format datetime
def format_datetime(dt_str):
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return dt_str

# Main function to run the Streamlit app
def main():
    st.title("Exemplar Prompt Hub")
    st.write("A modern interface for managing AI prompts.")

    # Sidebar for navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["View Prompts", "Add Prompt", "Edit Prompt", "Delete Prompt"]
    )

    if page == "View Prompts":
        st.header("View Prompts")
        prompts = fetch_prompts()
        
        if prompts:
            for prompt in prompts:
                with st.expander(f"{prompt['name']} (v{prompt['version']})"):
                    st.write(f"**Text:** {prompt['text']}")
                    st.write(f"**Description:** {prompt['description']}")
                    st.write(f"**Version:** {prompt['version']}")
                    st.write(f"**Created:** {format_datetime(prompt['created_at'])}")
                    if prompt.get('updated_at'):
                        st.write(f"**Last Updated:** {format_datetime(prompt['updated_at'])}")
                    if prompt.get('tags'):
                        st.write("**Tags:** " + ", ".join(tag['name'] for tag in prompt['tags']))
                    if prompt.get('meta'):
                        st.write("**Metadata:**")
                        st.json(prompt['meta'])
        else:
            st.info("No prompts found. Add some prompts to get started!")

    elif page == "Add Prompt":
        st.header("Add New Prompt")
        with st.form("add_prompt_form"):
            name = st.text_input("Name")
            text = st.text_area("Text")
            description = st.text_area("Description")
            tags = st.text_input("Tags (comma-separated)")
            meta = st.text_area("Meta (JSON format)", value="{}")
            
            submitted = st.form_submit_button("Add Prompt")
            if submitted:
                if not name or not text:
                    st.error("Name and text are required!")
                else:
                    try:
                        meta_json = json.loads(meta)
                        tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
                        add_prompt(name, text, description, meta_json, tags_list)
                    except json.JSONDecodeError:
                        st.error("Invalid JSON in meta field!")

    elif page == "Edit Prompt":
        st.header("Edit Prompt")
        prompts = fetch_prompts()
        prompt_options = {f"{p['name']} (ID: {p['id']})": p for p in prompts}
        selected = st.selectbox("Select a prompt to edit", list(prompt_options.keys())) if prompt_options else None
        if selected:
            prompt = prompt_options[selected]
            with st.form("edit_prompt_form"):
                st.write(f"**Current Version:** {prompt['version']}")
                text = st.text_area("Text", value=prompt['text'])
                description = st.text_area("Description", value=prompt['description'])
                tags = st.text_input("Tags (comma-separated)", value=", ".join(tag['name'] for tag in prompt.get('tags', [])))
                meta = st.text_area("Meta (JSON format)", value=json.dumps(prompt.get('meta', {}), indent=2))
                submitted = st.form_submit_button("Update Prompt")
                if submitted:
                    try:
                        meta_json = json.loads(meta)
                        tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
                        update_prompt(prompt['id'], text, description, meta_json, tags_list)
                    except json.JSONDecodeError:
                        st.error("Invalid JSON in meta field!")

    elif page == "Delete Prompt":
        st.header("Delete Prompt")
        prompts = fetch_prompts()
        prompt_options = {f"{p['name']} (ID: {p['id']})": p for p in prompts}
        selected = st.selectbox("Select a prompt to delete", list(prompt_options.keys())) if prompt_options else None
        if selected:
            prompt = prompt_options[selected]
            st.write(f"**Prompt Name:** {prompt['name']}")
            st.write(f"**Text:** {prompt['text']}")
            st.write(f"**Description:** {prompt['description']}")
            st.write(f"**Version:** {prompt['version']}")
            if st.button("Delete Prompt", key=f"delete_{prompt['id']}"):
                if st.confirm("Are you sure you want to delete this prompt?"):
                    delete_prompt(prompt['id'])

if __name__ == "__main__":
    main() 