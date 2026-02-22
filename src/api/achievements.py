from fastapi import APIRouter, HTTPException, status

from typing import List

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
async def create_achievement(achievement_AchievementCreate):
    global _next_id

    for ach in achievements_db.values():
        if ach.name == achievement_data.name:
            raise HTTPException(400, "Уже существует")

    new_ach = AchievementResponse(id=_next_id, name=achievement_data.name)
    achievements_db[_next_id] = new_ach
    _next_id += 1
    return new_ach


@router.delete("/{aid}", status_code=204)
async def delete_achievement(aid: int):
    if aid not in achievements_db:
        raise HTTPException(404, "Не найдено")
    del achievements_db[aid]
    return None
