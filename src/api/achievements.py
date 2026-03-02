from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.repositories.achievements import AchievementRepository
from src.schemas.achievements import AchievementCreate, AchievementResponse


router = APIRouter()

achievements_db: dict[int, AchievementResponse] = {}
_next_id = 1


@router.get("/", response_model=List[AchievementResponse])
async def get_achievements():
    return list(achievements_db.values())


@router.get("/{aid}", response_model=AchievementResponse)
async def get_achievement(aid: int):
    if aid not in achievements_db:
        raise HTTPException(404, "Достижение не найдено")
    return achievements_db[aid]


@router.post("/", response_model=AchievementResponse, status_code=201)
async def create_achievement(
    achievement_AchievementCreate, 
    db: Session = Depends(get_db)
):
    repo = AchievementRepository(db)
    
    if repo.name_exists(achievement_data.name):
        raise HTTPException(400, detail="Достижение уже существует")
    
    new_ach = repo.create({"name": achievement_data.name})
    return AchievementResponse.model_validate(new_ach)


@router.delete("/{aid}", status_code=204)
async def delete_achievement(aid: int):
    if aid not in achievements_db:
        raise HTTPException(404, "Не найдено")
    del achievements_db[aid]
    return None
