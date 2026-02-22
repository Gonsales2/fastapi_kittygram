from fastapi import APIRouter, HTTPException, status

from typing import List

from src.schemas.users import UserCreate, UserUpdate, UserResponse

router = APIRouter()

users_db: dict[int, UserResponse] = {}
_next_user_id = 1


@router.get("/", response_model=List[UserResponse])
async def get_all_users():
    return list(users_db.values())


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return users_db[user_id]


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user_UserCreate):
    global _next_user_id

    for user in users_db.values():
        if user.username == user_data.username:
            raise HTTPException(status_code=400, detail="Пользователь уже существует")

    new_user = UserResponse(
        id=_next_user_id,
        username=user_data.username,
        first_name=user_data.first_name or "",
        last_name=user_data.last_name or ""
    )
    users_db[_next_user_id] = new_user
    _next_user_id += 1
    return new_user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user = users_db[user_id]
    if user_data.username is not None:
        for u in users_db.values():
            if u.username == user_data.username and u.id != user_id:
                raise HTTPException(status_code=400, detail="Пользователь уже существует")
        user.username = user_data.username
    if user_data.first_name is not None:
        user.first_name = user_data.first_name
    if user_data.last_name is not None:
        user.last_name = user_data.last_name

    users_db[user_id] = user
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    del users_db[user_id]
    return None
