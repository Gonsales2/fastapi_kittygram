from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.base import TimestampMixin
from src.models.associations import cat_achievements 


class Cat(Base, TimestampMixin):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(16), nullable=False)
    color = Column(String(16), nullable=False)
    birth_year = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="cats")

    achievements = relationship(
        "Achievement",
        secondary=cat_achievements,
        back_populates="cats"
    )

    @property
    def age(self) -> int:
        from datetime import datetime
        return datetime.now().year - self.birth_year
