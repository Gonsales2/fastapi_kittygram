from fastapi import APIRouter, HTTPException, status

from typing import List

import datetime as dt

from src.schemas.cats import CatCreate, CatUpdate, CatResponse, CatColor

router = APIRouter()

cats_db: dict[int, CatResponse] = {}
_next_cat_id = 1


@router.get("/", response_model=List[CatResponse])
async def get_cats():
    return list(cats_db.values())


@router.get("/{cid}", response_model=CatResponse)
async def get_cat(cid: int):
    if cid not in cats_db:
        raise HTTPException(404, "Кошка не найдена")
    return cats_db[cid]


@router.post("/", response_model=CatResponse, status_code=201)
async def create_cat(cat_CatCreate):
    global _next_cat_id
    
    new_cat = CatResponse(
        id=_next_cat_id,
        owner_id=cat_data.owner_id,
        name=cat_data.name,
        color=cat_data.color,
        birth_year=cat_data.birth_year,
        achievements=cat_data.achievements or [],
        age=dt.datetime.now().year - cat_data.birth_year
    )
    cats_db[_next_cat_id] = new_cat
    _next_cat_id += 1
    return new_cat


@router.put("/{cid}", response_model=CatResponse)
async def update_cat(cid: int, cat_CatUpdate):
    if cid not in cats_db:
        raise HTTPException(404, "Кошка не найдена")
    
    cat = cats_db[cid]
    if cat_data.name is not None: cat.name = cat_data.name
    if cat_data.color is not None: cat.color = cat_data.color
    if cat_data.birth_year is not None:
        cat.birth_year = cat_data.birth_year
        cat.age = dt.datetime.now().year - cat_data.birth_year
    if cat_data.achievements is not None:
        cat.achievements = cat_data.achievements
    
    cats_db[cid] = cat
    return cat


@router.delete("/{cid}", status_code=204)
async def delete_cat(cid: int):
    if cid not in cats_db:
        raise HTTPException(404, "Кошка не найдена")
    del cats_db[cid]
    return None
