from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.prompt import Prompt, PromptCreate, PromptUpdate, Tag
from app.db.models import Prompt as PromptModel, Tag as TagModel, PromptVersion as PromptVersionModel
from sqlalchemy import or_, text
from app.core.config import settings
from app.scripts.seed_prompts_api import seed_prompts_api

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