from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from src.models.achievements import Achievement
from src.models.associations import cat_achievements
from src.models.cat import Cat
from src.repositories.base import BaseRepository


class AchievementRepository(BaseRepository[Achievement]):
    def __init__(self, db: Session):
        super().__init__(Achievement, db)

    def get_by_name(self, name: str) -> Optional[Achievement]:
        """Получить достижение по имени"""
        return (
            self.db.query(Achievement)
            .filter(func.lower(Achievement.name) == func.lower(name))
            .first()
        )

    def name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Проверить, существует ли достижение с таким именем"""
        query = self.db.query(Achievement).filter(
            func.lower(Achievement.name) == func.lower(name)
        )
        if exclude_id is not None:
            query = query.filter(Achievement.id != exclude_id)
        return query.first() is not None

    def get_achievements_for_cat(self, cat_id: int) -> List[Achievement]:
        """Получить все достижения конкретной кошки"""
        return (
            self.db.query(Achievement)
            .join(cat_achievements)
            .filter(cat_achievements.c.cat_id == cat_id)
            .all()
        )

    def add_achievement_to_cat(self, cat_id: int, achievement_id: int) -> bool:
        """Привязать достижение к кошке"""
        cat = self.db.query(Cat).filter(Cat.id == cat_id).first()
        achievement = self.get(achievement_id)
        
        if not cat or not achievement:
            return False
        
        exists = (
            self.db.query(cat_achievements)
            .filter(
                cat_achievements.c.cat_id == cat_id,
                cat_achievements.c.achievement_id == achievement_id
            )
            .first()
        )
        if exists:
            return True
        
        link = cat_achievements.insert().values(
            cat_id=cat_id,
            achievement_id=achievement_id
        )
        self.db.execute(link)
        self.db.commit()
        return True

    def remove_achievement_from_cat(self, cat_id: int, achievement_id: int) -> bool:
        """Отвязать достижение от кошки"""
        result = (
            self.db.query(cat_achievements)
            .filter(
                cat_achievements.c.cat_id == cat_id,
                cat_achievements.c.achievement_id == achievement_id
            )
            .delete()
        )
        self.db.commit()
        return result > 0

    def search(self, query: str, limit: int = 20) -> List[Achievement]:
        """Поиск достижений по подстроке"""
        return (
            self.db.query(Achievement)
            .filter(Achievement.name.ilike(f"%{query}%"))
            .limit(limit)
            .all()
        )
