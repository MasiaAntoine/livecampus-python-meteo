from pydantic import BaseModel
from datetime import datetime

class UserHistoryBase(BaseModel):
    city: str
    latitude: float
    longitude: float
    temperature: float

class UserHistoryCreate(UserHistoryBase):
    pass

class UserHistory(UserHistoryBase):
    id: int
    user_id: int
    search_date: datetime

    class Config:
        orm_mode = True
