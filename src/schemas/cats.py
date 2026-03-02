from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Literal, Optional, List

CatColor = Literal["Gray", "Black", "White", "Ginger", "Mixed"]


class CatBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=16)
    color: CatColor
    birth_year: int = Field(..., ge=1900, le=2100)


class CatCreate(CatBase):
    owner_id: int
    achievements: Optional[List[str]] = Field(default_factory=list)


class CatUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=16)
    color: Optional[CatColor] = None
    birth_year: Optional[int] = Field(None, ge=1900, le=2100)
    achievements: Optional[List[str]] = None


class CatResponse(CatBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    owner_id: int
    achievements: List[str] = Field(default_factory=list)
    age: int

    @field_validator("color", mode="before")
    @classmethod
    def normalize_color(cls, value):
        if isinstance(value, str):
            normalized = value.capitalize() if value.lower() != "ginger" else "Ginger"
            if normalized in ["Gray", "Black", "White", "Ginger", "Mixed"]:
                return normalized
        return value