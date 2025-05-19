import pytest
from fastapi import status


def test_create_prompt(client, test_prompt_data):
    response = client.post("/api/v1/prompts/", json=test_prompt_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == test_prompt_data["name"]
    assert data["text"] == test_prompt_data["text"]
    assert data["description"] == test_prompt_data["description"]
    assert data["version"] == 1  # Always starts with version 1
    assert data["meta"] == test_prompt_data["meta"]
    assert len(data["tags"]) == len(test_prompt_data["tags"])


def test_create_duplicate_prompt(client, test_prompt):
    # Remove any fields that aren't in PromptCreate schema
    create_data = {
        "name": test_prompt["name"],
        "text": test_prompt["text"],
        "description": test_prompt["description"],
        "meta": test_prompt["meta"],
        "tags": test_prompt["tags"]
    }
    response = client.post("/api/v1/prompts/", json=create_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


def test_read_prompts(client, test_prompt):
    response = client.get("/api/v1/prompts/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == test_prompt["name"]


def test_read_prompts_with_search(client, test_prompt):
    response = client.get("/api/v1/prompts/?search=test")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == test_prompt["name"]


def test_read_prompts_with_tag(client, test_prompt):
    response = client.get("/api/v1/prompts/?tag=test")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == test_prompt["name"]


def test_read_prompt(client, test_prompt):
    response = client.get(f"/api/v1/prompts/{test_prompt['id']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == test_prompt["name"]


def test_read_nonexistent_prompt(client):
    response = client.get("/api/v1/prompts/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_prompt_with_version(client, test_prompt):
    update_data = {
        "text": "Updated test prompt",
        "description": "Updated description",
        "version": 2,
        "tags": ["test", "updated"]
    }
    response = client.put(f"/api/v1/prompts/{test_prompt['id']}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["text"] == update_data["text"]
    assert data["description"] == update_data["description"]
    assert data["version"] == update_data["version"]
    assert len(data["tags"]) == len(update_data["tags"])


def test_update_prompt_without_version(client, test_prompt):
    # First update without version
    update_data = {
        "text": "Updated test prompt",
        "description": "Updated description",
        "tags": ["test", "updated"]
    }
    response = client.put(f"/api/v1/prompts/{test_prompt['id']}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["version"] == 2  # Should auto-increment from 1 to 2
    
    # Second update without version
    update_data = {
        "text": "Another update",
        "description": "Another description"
    }
    response = client.put(f"/api/v1/prompts/{test_prompt['id']}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["version"] == 3  # Should auto-increment from 2 to 3


def test_update_prompt_with_invalid_version(client, test_prompt):
    # Update with non-integer version
    update_data = {
        "text": "Updated test prompt",
        "version": "invalid"
    }
    response = client.put(f"/api/v1/prompts/{test_prompt['id']}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["version"] == 1  # Should reset to 1 for invalid version


def test_update_nonexistent_prompt(client):
    update_data = {"text": "Updated test prompt"}
    response = client.put("/api/v1/prompts/999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_prompt(client, test_prompt):
    response = client.delete(f"/api/v1/prompts/{test_prompt['id']}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Prompt deleted successfully"

    # Verify prompt is deleted
    response = client.get(f"/api/v1/prompts/{test_prompt['id']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_prompt(client):
    response = client.delete("/api/v1/prompts/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND 