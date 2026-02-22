from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

import datetime as dt


class CatColor(str, Enum):
    GRAY = "Gray"
    BLACK = "Black"
    WHITE = "White"
    GINGER = "Ginger"
    MIXED = "Mixed"


class User(BaseModel):
    """Модель пользователя"""
    id: Optional[int] = None
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Achievement(BaseModel):
    """Модель достижения"""
    id: Optional[int] = None
    name: str


class AchievementCat(BaseModel):
    """Связующая модель AchievementCat"""
    id: Optional[int] = None
    achievement: Achievement
    cat_id: int


class Cat(BaseModel):
    """Модель кошки"""
    id: Optional[int] = None
    name: str = Field(..., max_length=16)
    color: CatColor
    birth_year: int
    owner: User
    achievements: List[Achievement] = []
