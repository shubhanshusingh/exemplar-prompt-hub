import pytest
from datetime import datetime
from app.db.models import Prompt, Tag, PromptVersion
from sqlalchemy.exc import IntegrityError

def test_create_prompt(db_session):
    """Test creating a basic prompt."""
    prompt = Prompt(
        name="test-prompt",
        text="Test prompt text",
        description="Test description",
        version=1,
        meta={"author": "test-user"}
    )
    db_session.add(prompt)
    db_session.commit()
    db_session.refresh(prompt)

    assert prompt.id is not None
    assert prompt.name == "test-prompt"
    assert prompt.text == "Test prompt text"
    assert prompt.description == "Test description"
    assert prompt.version == 1
    assert prompt.meta == {"author": "test-user"}
    assert isinstance(prompt.created_at, datetime)
    assert prompt.updated_at is None

def test_create_prompt_with_tags(db_session):
    """Test creating a prompt with tags."""
    # Create tags first
    tag1 = Tag(name="test-tag-1")
    tag2 = Tag(name="test-tag-2")
    db_session.add_all([tag1, tag2])
    db_session.commit()

    # Create prompt with tags
    prompt = Prompt(
        name="test-prompt-with-tags",
        text="Test prompt text",
        version=1
    )
    prompt.tags.extend([tag1, tag2])
    db_session.add(prompt)
    db_session.commit()
    db_session.refresh(prompt)

    assert len(prompt.tags) == 2
    assert {tag.name for tag in prompt.tags} == {"test-tag-1", "test-tag-2"}

def test_create_prompt_version(db_session):
    """Test creating a prompt version."""
    # Create prompt
    prompt = Prompt(
        name="test-prompt",
        text="Test prompt text",
        version=1
    )
    db_session.add(prompt)
    db_session.commit()

    # Create version
    version = PromptVersion(
        prompt_id=prompt.id,
        version=2,
        text="Updated prompt text",
        description="Updated description",
        meta={"changes": "Updated text"}
    )
    db_session.add(version)
    db_session.commit()
    db_session.refresh(version)

    assert version.id is not None
    assert version.prompt_id == prompt.id
    assert version.version == 2
    assert version.text == "Updated prompt text"
    assert version.description == "Updated description"
    assert version.meta == {"changes": "Updated text"}
    assert isinstance(version.created_at, datetime)

def test_prompt_unique_name_constraint(db_session):
    """Test that prompt names must be unique."""
    # Create first prompt
    prompt1 = Prompt(
        name="test-prompt",
        text="Test prompt text",
        version=1
    )
    db_session.add(prompt1)
    db_session.commit()

    # Try to create second prompt with same name
    prompt2 = Prompt(
        name="test-prompt",
        text="Another test prompt text",
        version=1
    )
    db_session.add(prompt2)
    
    with pytest.raises(IntegrityError):
        db_session.commit()
    
    db_session.rollback()

def test_prompt_version_relationship(db_session):
    """Test the relationship between prompts and their versions."""
    # Create prompt
    prompt = Prompt(
        name="test-prompt",
        text="Test prompt text",
        version=1
    )
    db_session.add(prompt)
    db_session.commit()

    # Create multiple versions
    versions = [
        PromptVersion(
            prompt_id=prompt.id,
            version=i,
            text=f"Version {i} text",
            meta={"version": i}
        )
        for i in range(1, 4)
    ]
    db_session.add_all(versions)
    db_session.commit()
    db_session.refresh(prompt)

    assert len(prompt.versions) == 3
    assert {v.version for v in prompt.versions} == {1, 2, 3}
    assert all(isinstance(v, PromptVersion) for v in prompt.versions)

def test_prompt_tag_relationship(db_session):
    """Test the many-to-many relationship between prompts and tags."""
    # Create tags
    tags = [Tag(name=f"tag-{i}") for i in range(3)]
    db_session.add_all(tags)
    db_session.commit()

    # Create prompt with tags
    prompt = Prompt(
        name="test-prompt",
        text="Test prompt text",
        version=1
    )
    prompt.tags.extend(tags)
    db_session.add(prompt)
    db_session.commit()
    db_session.refresh(prompt)

    # Verify relationships
    assert len(prompt.tags) == 3
    assert {tag.name for tag in prompt.tags} == {"tag-0", "tag-1", "tag-2"}
    
    # Verify tag relationships
    for tag in tags:
        db_session.refresh(tag)
        assert len(tag.prompts) == 1
        assert tag.prompts[0].id == prompt.id 