from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.base import TimestampMixin
from src.models.associations import cat_achievements 


class Achievement(Base, TimestampMixin):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, nullable=False)

    cats = relationship(
        "Cat",
        secondary=cat_achievements,
        back_populates="achievements"
    )
