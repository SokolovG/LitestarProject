from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    """Regular user schema."""
    id: int
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(min_length=3, max_length=30)
    last_name: str = Field(min_length=3, max_length=30)

    class Config:
        from_attributes = True


class UpdateUserSchema(BaseModel):
    """User schema for update data."""
    username: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(min_length=3, max_length=30)
    last_name: str = Field(min_length=3, max_length=30)


class UserLoginSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
