import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.models import Prompt, Tag, PromptVersion

@pytest.fixture
def test_prompt_data():
    return {
        "name": "test-prompt",
        "text": "Test prompt text",
        "description": "Test description",
        "version": 1,
        "meta": {"author": "test-user"},
        "tags": ["test-tag-1", "test-tag-2"]
    }

def test_create_prompt(client, test_prompt_data):
    """Test creating a new prompt via API."""
    response = client.post("/api/v1/prompts/", json=test_prompt_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["name"] == test_prompt_data["name"]
    assert data["text"] == test_prompt_data["text"]
    assert data["description"] == test_prompt_data["description"]
    assert data["version"] == test_prompt_data["version"]
    assert data["meta"] == test_prompt_data["meta"]
    assert len(data["tags"]) == 2
    assert {tag["name"] for tag in data["tags"]} == set(test_prompt_data["tags"])

def test_create_duplicate_prompt(client, test_prompt_data):
    """Test that creating a prompt with duplicate name fails."""
    # Create first prompt
    response = client.post("/api/v1/prompts/", json=test_prompt_data)
    assert response.status_code == 200
    
    # Try to create duplicate prompt
    response = client.post("/api/v1/prompts/", json=test_prompt_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_get_prompt(client, test_prompt_data):
    """Test retrieving a prompt by ID."""
    # Create a prompt first
    create_response = client.post("/api/v1/prompts/", json=test_prompt_data)
    prompt_id = create_response.json()["id"]
    
    # Get the prompt
    response = client.get(f"/api/v1/prompts/{prompt_id}")
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == prompt_id
    assert data["name"] == test_prompt_data["name"]
    assert data["text"] == test_prompt_data["text"]

def test_get_nonexistent_prompt(client):
    """Test retrieving a non-existent prompt."""
    response = client.get("/api/v1/prompts/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_list_prompts(client, test_prompt_data):
    """Test listing prompts with pagination and search."""
    # Create multiple prompts
    prompts = []
    for i in range(3):
        prompt_data = test_prompt_data.copy()
        prompt_data["name"] = f"test-prompt-{i}"
        response = client.post("/api/v1/prompts/", json=prompt_data)
        prompts.append(response.json())
    
    # Test basic listing
    response = client.get("/api/v1/prompts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    
    # Test search
    response = client.get("/api/v1/prompts/?search=test-prompt-1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "test-prompt-1"
    
    # Test tag filtering
    response = client.get("/api/v1/prompts/?tag=test-tag-1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3  # All prompts have this tag

def test_update_prompt(client, test_prompt_data):
    """Test updating a prompt."""
    # Create a prompt first
    create_response = client.post("/api/v1/prompts/", json=test_prompt_data)
    prompt_id = create_response.json()["id"]
    
    # Update the prompt
    update_data = {
        "name": "updated-prompt",
        "text": "Updated prompt text",
        "description": "Updated description",
        "version": 2,
        "meta": {"author": "test-user", "updated": True},
        "tags": ["test-tag-1", "test-tag-3"]
    }
    
    response = client.put(f"/api/v1/prompts/{prompt_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["name"] == update_data["name"]
    assert data["text"] == update_data["text"]
    assert data["description"] == update_data["description"]
    assert data["version"] == update_data["version"]
    assert data["meta"] == update_data["meta"]
    assert len(data["tags"]) == 2
    assert {tag["name"] for tag in data["tags"]} == set(update_data["tags"])

def test_update_prompt_duplicate_name(client, test_prompt_data):
    """Test that updating a prompt with a duplicate name fails."""
    # Create first prompt
    response = client.post("/api/v1/prompts/", json=test_prompt_data)
    assert response.status_code == 200
    
    # Create second prompt
    second_prompt_data = test_prompt_data.copy()
    second_prompt_data["name"] = "test-prompt-2"
    response = client.post("/api/v1/prompts/", json=second_prompt_data)
    assert response.status_code == 200
    second_prompt_id = response.json()["id"]
    
    # Try to update second prompt with first prompt's name
    update_data = {"name": test_prompt_data["name"]}
    response = client.put(f"/api/v1/prompts/{second_prompt_id}", json=update_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_delete_prompt(client, test_prompt_data):
    """Test deleting a prompt."""
    # Create a prompt first
    create_response = client.post("/api/v1/prompts/", json=test_prompt_data)
    prompt_id = create_response.json()["id"]
    
    # Delete the prompt
    response = client.delete(f"/api/v1/prompts/{prompt_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Prompt deleted successfully"
    
    # Verify prompt is deleted
    get_response = client.get(f"/api/v1/prompts/{prompt_id}")
    assert get_response.status_code == 404 