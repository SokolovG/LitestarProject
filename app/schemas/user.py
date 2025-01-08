from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    """Regular user schema."""
    id: int
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr

    class Config:
        from_attributes = True


class UpdateUserSchema(BaseModel):
    """User schema for update data."""
    username: str | None = None
    email: EmailStr | None = None
