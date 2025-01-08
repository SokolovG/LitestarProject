from pydantic import BaseModel, EmailStr, Field


class CreateUserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr


class UpdateUserSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
