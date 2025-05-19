import pytest
from fastapi import status


def test_create_prompt(client, test_prompt_data):
    response = client.post("/api/v1/prompts/", json=test_prompt_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == test_prompt_data["name"]
    assert data["text"] == test_prompt_data["text"]
    assert data["description"] == test_prompt_data["description"]
    assert data["version"] == test_prompt_data["version"]
    assert data["meta"] == test_prompt_data["meta"]
    assert len(data["tags"]) == len(test_prompt_data["tags"])


def test_create_duplicate_prompt(client, test_prompt):
    response = client.post("/api/v1/prompts/", json=test_prompt)
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


def test_update_prompt(client, test_prompt):
    update_data = {
        "text": "Updated test prompt",
        "description": "Updated description",
        "version": "1.0.1",
        "tags": ["test", "updated"]
    }
    response = client.put(f"/api/v1/prompts/{test_prompt['id']}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["text"] == update_data["text"]
    assert data["description"] == update_data["description"]
    assert data["version"] == update_data["version"]
    assert len(data["tags"]) == len(update_data["tags"])


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