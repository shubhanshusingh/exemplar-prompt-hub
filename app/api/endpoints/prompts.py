from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.prompt import (
    Prompt, PromptCreate, PromptUpdate, Tag, PromptVersion,
    PlaygroundRequest, PlaygroundResponse
)
from app.db.models import Prompt as PromptModel, Tag as TagModel, PromptVersion as PromptVersionModel
from sqlalchemy import or_, text
from app.core.config import settings
from app.scripts.seed_prompts_api import seed_prompts_api
import httpx
import json

router = APIRouter()


@router.post("/", response_model=Prompt)
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    # Check for duplicate prompt name first
    existing_prompt = db.query(PromptModel).filter(PromptModel.name == prompt.name).first()
    if existing_prompt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A prompt with this name already exists"
        )
    
    # Create new prompt with version 1
    db_prompt = PromptModel(
        name=prompt.name,
        text=prompt.text,
        description=prompt.description,
        version=1,  # Always start with version 1 as integer
        meta=prompt.meta
    )
    
    # Handle tags
    if prompt.tags:
        for tag_name in prompt.tags:
            tag = db.query(TagModel).filter(TagModel.name == tag_name).first()
            if not tag:
                tag = TagModel(name=tag_name)
                db.add(tag)
            db_prompt.tags.append(tag)
    
    db.add(db_prompt)
    db.flush()  # Ensure tag gets an id
    
    # Create initial version
    version = PromptVersionModel(
        prompt_id=db_prompt.id,
        version=1,
        text=prompt.text,
        description=prompt.description,
        meta=prompt.meta
    )
    db.add(version)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


@router.get("/", response_model=List[Prompt])
def read_prompts(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    tag: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(PromptModel)
    
    if search:
        query = query.filter(PromptModel.name.ilike(f"%{search}%"))
    
    if tag:
        query = query.join(PromptModel.tags).filter(TagModel.name == tag)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{prompt_id}", response_model=Prompt)
def read_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.query(PromptModel).filter(PromptModel.id == prompt_id).first()
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@router.put("/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: int, prompt: PromptUpdate, db: Session = Depends(get_db)):
    db_prompt = db.query(PromptModel).filter(PromptModel.id == prompt_id).first()
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Check for duplicate name if name is being updated
    if prompt.name is not None and prompt.name != db_prompt.name:
        existing_prompt = db.query(PromptModel).filter(PromptModel.name == prompt.name).first()
        if existing_prompt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A prompt with this name already exists"
            )
    
    # Handle version
    if prompt.version is not None:
        try:
            version = int(prompt.version)
            if version <= 0:
                version = 1
        except (ValueError, TypeError):
            version = db_prompt.version + 1
    else:
        version = db_prompt.version + 1
    
    # Update prompt fields
    for field, value in prompt.model_dump(exclude_unset=True).items():
        if field != "version" and field != "tags":
            setattr(db_prompt, field, value)
    
    # Handle tags
    if prompt.tags is not None:
        db_prompt.tags = []
        for tag_name in prompt.tags:
            tag = db.query(TagModel).filter(TagModel.name == tag_name).first()
            if not tag:
                tag = TagModel(name=tag_name)
                db.add(tag)
            db_prompt.tags.append(tag)
    
    # Update version
    db_prompt.version = version
    
    # Create new version record
    version = PromptVersionModel(
        prompt_id=db_prompt.id,
        version=version,
        text=db_prompt.text,
        description=db_prompt.description,
        meta=db_prompt.meta
    )
    db.add(version)
    
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


@router.delete("/{prompt_id}")
def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.query(PromptModel).filter(PromptModel.id == prompt_id).first()
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    db.delete(prompt)
    db.commit()
    return {"message": "Prompt deleted successfully"}

@router.post("/seed", status_code=status.HTTP_201_CREATED)
def seed_database():
    """
    Seed the database with initial prompt data.
    This endpoint is used to populate the database with sample prompts.
    """
    try:
        seed_prompts_api()
        return {"message": "Database seeded successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to seed database: {str(e)}"
        )

@router.get("/{prompt_id}/versions/{version_number}", response_model=PromptVersion)
def read_prompt_version(prompt_id: int, version_number: int, db: Session = Depends(get_db)):
    """
    Fetch a specific version of a prompt.
    """
    # First check if prompt exists
    prompt = db.query(PromptModel).filter(PromptModel.id == prompt_id).first()
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Get the specific version
    version = db.query(PromptVersionModel).filter(
        PromptVersionModel.prompt_id == prompt_id,
        PromptVersionModel.version == version_number
    ).first()
    
    if version is None:
        raise HTTPException(
            status_code=404,
            detail=f"Version {version_number} not found for prompt {prompt_id}"
        )
    
    return version

@router.post("/playground", response_model=PlaygroundResponse)
async def prompt_playground(
    request: PlaygroundRequest,
    db: Session = Depends(get_db)
):
    """
    Compare responses from different LLM models for a given prompt.
    
    Args:
        request: PlaygroundRequest containing prompt_id, models, variables, and optional version
        db: Database session
    
    Returns:
        PlaygroundResponse containing responses from each model
    """
    # Get the prompt
    prompt = db.query(PromptModel).filter(PromptModel.id == request.prompt_id).first()
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Get the prompt version if specified, otherwise use latest
    prompt_version = prompt.version
    if request.version is not None:
        version = db.query(PromptVersionModel).filter(
            PromptVersionModel.prompt_id == request.prompt_id,
            PromptVersionModel.version == request.version
        ).first()
        if version is None:
            raise HTTPException(
                status_code=404,
                detail=f"Version {request.version} not found for prompt {request.prompt_id}"
            )
        prompt_text = version.text
        prompt_version = version.version
    else:
        prompt_text = prompt.text
    
    # Prepare the prompt text with variables if provided
    if request.variables:
        try:
            # Simple variable substitution
            for key, value in request.variables.items():
                prompt_text = prompt_text.replace(f"{{{{ {key} }}}}", str(value))
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error processing variables: {str(e)}"
            )
    
    # Get responses from each model
    responses = {}
    async with httpx.AsyncClient() as client:
        for model in request.models:
            try:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                        "HTTP-Referer": settings.PROJECT_URL,  # Optional: for rankings
                        "X-Title": settings.PROJECT_NAME,  # Optional: for rankings
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are a helpful AI assistant."},
                            {"role": "user", "content": prompt_text}
                        ]
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                responses[model] = {
                    "response": result["choices"][0]["message"]["content"],
                    "model": model,
                    "prompt_used": prompt_text,
                    "metadata": {
                        "prompt_id": request.prompt_id,
                        "prompt_version": prompt_version,
                        "variables_used": request.variables,
                        "usage": result.get("usage", {}),
                        "model_info": result.get("model", {})
                    }
                }
            except Exception as e:
                responses[model] = {
                    "error": str(e),
                    "model": model,
                    "prompt_used": prompt_text
                }
    
    return PlaygroundResponse(
        prompt_id=request.prompt_id,
        prompt_name=prompt.name,
        prompt_version=prompt_version,
        variables_used=request.variables,
        responses=responses
    ) 