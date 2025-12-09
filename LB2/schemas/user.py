from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1)

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None

class UserResponse(UserBase):
    id: int
