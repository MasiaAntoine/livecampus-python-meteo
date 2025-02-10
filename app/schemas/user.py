from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str
    email: str
    access_token: str | None = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    access_token: str | None = None

class User(UserBase):
    id: int

    class Config:
        config_dict = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str