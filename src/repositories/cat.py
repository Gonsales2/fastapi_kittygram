from sqlalchemy.orm import Session
from src.models.cat import Cat
from src.repositories.base import BaseRepository
from typing import List, Optional


class CatRepository(BaseRepository[Cat]):
    def __init__(self, db: Session):
        super().__init__(Cat, db)

    def get_by_owner(self, owner_id: int) -> List[Cat]:
        return self.db.query(Cat).filter(Cat.owner_id == owner_id).all()

    def get_by_color(self, color: str) -> List[Cat]:
        return self.db.query(Cat).filter(Cat.color == color).all()
