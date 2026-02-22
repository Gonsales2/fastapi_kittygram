from pydantic import BaseModel, Field, ConfigDict


class AchievementBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)


class AchievementCreate(AchievementBase):
    pass


class AchievementResponse(AchievementBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
