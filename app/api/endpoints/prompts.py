from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.prompt import Prompt, PromptCreate, PromptUpdate, Tag
from app.db.models import Prompt as PromptModel, Tag as TagModel
from sqlalchemy import or_
from app.scripts.seed_prompts_api import seed_prompts_api  # Import the seed function

router = APIRouter()


@router.post("/", response_model=Prompt)
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    # Check if prompt with same name exists
    db_prompt = db.query(PromptModel).filter(PromptModel.name == prompt.name).first()
    if db_prompt:
        raise HTTPException(status_code=400, detail="Prompt with this name already exists")
    
    # Create new prompt
    db_prompt = PromptModel(
        name=prompt.name,
        text=prompt.text,
        description=prompt.description,
        version=prompt.version,
        meta=prompt.meta
    )
    
    # Add tags
    if prompt.tags:
        for tag_name in prompt.tags:
            db_tag = db.query(TagModel).filter(TagModel.name == tag_name).first()
            if not db_tag:
                db_tag = TagModel(name=tag_name)
                db.add(db_tag)
            db_prompt.tags.append(db_tag)
    
    db.add(db_prompt)
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
        query = query.filter(
            or_(
                PromptModel.name.ilike(f"%{search}%"),
                PromptModel.description.ilike(f"%{search}%"),
                PromptModel.text.ilike(f"%{search}%")
            )
        )
    
    if tag:
        query = query.join(PromptModel.tags).filter(TagModel.name == tag)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{prompt_id}", response_model=Prompt)
def read_prompt(prompt_id: int, db: Session = Depends(get_db)):
    db_prompt = db.query(PromptModel).filter(PromptModel.id == prompt_id).first()
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return db_prompt


@router.put("/{prompt_id}", response_model=Prompt)
def update_prompt(
    prompt_id: int,
    prompt: PromptUpdate,
    db: Session = Depends(get_db)
):
    db_prompt = db.query(PromptModel).filter(PromptModel.id == prompt_id).first()
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Update prompt fields
    for field, value in prompt.dict(exclude_unset=True).items():
        if field != "tags":
            setattr(db_prompt, field, value)
    
    # Update tags if provided
    if prompt.tags is not None:
        db_prompt.tags = []
        for tag_name in prompt.tags:
            db_tag = db.query(TagModel).filter(TagModel.name == tag_name).first()
            if not db_tag:
                db_tag = TagModel(name=tag_name)
                db.add(db_tag)
            db_prompt.tags.append(db_tag)
    
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


@router.delete("/{prompt_id}")
def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    db_prompt = db.query(PromptModel).filter(PromptModel.id == prompt_id).first()
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    db.delete(db_prompt)
    db.commit()
    return {"message": "Prompt deleted successfully"}

@router.post("/seed")
def seed_database():
    seed_prompts_api()  # Call the seed function
    return {"message": "Database seeded successfully"} 