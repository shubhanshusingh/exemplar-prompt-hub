import pytest
from datetime import datetime
from app.db.models import Prompt, Tag, PromptVersion


def test_create_prompt(db_session):
    # Create a prompt
    prompt = Prompt(
        name="test-prompt",
        text="Test prompt text",
        description="Test description",
        version="1.0.0",
        meta={"author": "test-user"}
    )
    db_session.add(prompt)
    db_session.commit()
    db_session.refresh(prompt)

    assert prompt.id is not None
    assert prompt.name == "test-prompt"
    assert prompt.text == "Test prompt text"
    assert prompt.description == "Test description"
    assert prompt.version == "1.0.0"
    assert prompt.meta == {"author": "test-user"}
    assert isinstance(prompt.created_at, datetime)
    assert prompt.updated_at is None


def test_create_prompt_with_tags(db_session):
    # Create tags
    tag1 = Tag(name="test")
    tag2 = Tag(name="example")
    db_session.add_all([tag1, tag2])
    db_session.commit()

    # Create prompt with tags
    prompt = Prompt(
        name="test-prompt",
        text="Test prompt text",
        version="1.0.0"
    )
    prompt.tags.extend([tag1, tag2])
    db_session.add(prompt)
    db_session.commit()
    db_session.refresh(prompt)

    assert len(prompt.tags) == 2
    assert {tag.name for tag in prompt.tags} == {"test", "example"}


def test_create_prompt_version(db_session):
    # Create prompt
    prompt = Prompt(
        name="test-prompt",
        text="Test prompt text",
        version="1.0.0"
    )
    db_session.add(prompt)
    db_session.commit()

    # Create version
    version = PromptVersion(
        prompt_id=prompt.id,
        version="1.0.1",
        text="Updated prompt text",
        meta={"changes": "Updated text"}
    )
    db_session.add(version)
    db_session.commit()
    db_session.refresh(version)

    assert version.id is not None
    assert version.prompt_id == prompt.id
    assert version.version == "1.0.1"
    assert version.text == "Updated prompt text"
    assert version.meta == {"changes": "Updated text"}
    assert isinstance(version.created_at, datetime)


def test_prompt_relationships(db_session):
    # Create prompt
    prompt = Prompt(
        name="test-prompt",
        text="Test prompt text",
        version="1.0.0"
    )
    db_session.add(prompt)
    db_session.commit()

    # Create versions
    version1 = PromptVersion(
        prompt_id=prompt.id,
        version="1.0.1",
        text="Updated text 1"
    )
    version2 = PromptVersion(
        prompt_id=prompt.id,
        version="1.0.2",
        text="Updated text 2"
    )
    db_session.add_all([version1, version2])
    db_session.commit()
    db_session.refresh(prompt)

    assert len(prompt.versions) == 2
    assert {v.version for v in prompt.versions} == {"1.0.1", "1.0.2"}


def test_unique_prompt_name(db_session):
    # Create first prompt
    prompt1 = Prompt(
        name="test-prompt",
        text="Test prompt text",
        version="1.0.0"
    )
    db_session.add(prompt1)
    db_session.commit()

    # Try to create prompt with same name
    prompt2 = Prompt(
        name="test-prompt",
        text="Another prompt text",
        version="1.0.0"
    )
    db_session.add(prompt2)
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an integrity error
        db_session.commit()
    
    db_session.rollback()


def test_unique_tag_name(db_session):
    # Create first tag
    tag1 = Tag(name="test")
    db_session.add(tag1)
    db_session.commit()

    # Try to create tag with same name
    tag2 = Tag(name="test")
    db_session.add(tag2)
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an integrity error
        db_session.commit()
    
    db_session.rollback() 