from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
import datetime as dt

from src.schemas.cats import CatCreate, CatUpdate, CatResponse, CatColor
from src.database import get_db
from src.repositories.cat import CatRepository
from src.repositories.user import UserRepository

router = APIRouter()


@router.get("/", response_model=List[CatResponse])
async def get_cats(db: Session = Depends(get_db)):
    repo = CatRepository(db)
    cats = repo.get_all()
    return [CatResponse.model_validate(cat) for cat in cats]


@router.get("/{cid}", response_model=CatResponse)
async def get_cat(cid: int, db: Session = Depends(get_db)):
    repo = CatRepository(db)
    cat = repo.get(cid)
    if not cat:
        raise HTTPException(404, detail="Кошка не найдена")
    return CatResponse.model_validate(cat)


@router.post("/", response_model=CatResponse, status_code=201)
async def create_cat(cat_data: CatCreate, db: Session = Depends(get_db)):
    # Проверяем существование владельца
    user_repo = UserRepository(db)
    if not user_repo.get(cat_data.owner_id):
        raise HTTPException(404, detail="Владелец не найден")
    
    cat_repo = CatRepository(db)
    
    # Создаём кошку
    cat_dict = cat_data.model_dump(exclude={"achievements"})
    new_cat = cat_repo.create(cat_dict)
    
    # Здесь можно добавить логику для achievements
    return CatResponse.model_validate(new_cat)


@router.put("/{cid}", response_model=CatResponse)
async def update_cat(cid: int, cat_data: CatUpdate, db: Session = Depends(get_db)):
    repo = CatRepository(db)
    updated = repo.update(cid, cat_data.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(404, detail="Кошка не найдена")
    return CatResponse.model_validate(updated)


@router.delete("/{cid}", status_code=204)
async def delete_cat(cid: int, db: Session = Depends(get_db)):
    repo = CatRepository(db)
    if not repo.delete(cid):
        raise HTTPException(404, detail="Кошка не найдена")
    return None