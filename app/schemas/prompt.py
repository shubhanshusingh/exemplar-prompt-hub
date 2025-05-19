from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True


class PromptVersionBase(BaseModel):
    version: str
    text: str
    meta: Optional[Dict[str, Any]] = None


class PromptVersionCreate(PromptVersionBase):
    pass


class PromptVersion(PromptVersionBase):
    id: int
    prompt_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PromptBase(BaseModel):
    name: str
    text: str
    description: Optional[str] = None
    version: str
    meta: Optional[Dict[str, Any]] = None


class PromptCreate(PromptBase):
    tags: Optional[List[str]] = None


class PromptUpdate(BaseModel):
    text: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None


class Prompt(PromptBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: List[Tag] = []
    versions: List[PromptVersion] = []

    class Config:
        from_attributes = True 