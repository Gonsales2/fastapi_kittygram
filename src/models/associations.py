from sqlalchemy import Column, Integer, ForeignKey, Table
from src.database import Base


cat_achievements = Table(
    "cat_achievements",
    Base.metadata,
    Column("cat_id", Integer, ForeignKey("cats.id"), primary_key=True),
    Column("achievement_id", Integer, ForeignKey("achievements.id"), primary_key=True),
)
