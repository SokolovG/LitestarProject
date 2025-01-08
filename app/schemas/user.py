from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr

    class Config:
        from_attributes = True

class UpdateUserSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
