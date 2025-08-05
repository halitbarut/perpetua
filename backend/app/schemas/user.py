from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    weekly_score: int
    current_level: str

    class Config:
        from_attributes = True

class UserLevelUpdate(BaseModel):
    level: str