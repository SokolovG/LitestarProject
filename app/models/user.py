from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description='Username', examples=['Jonn_lennon'])

    first_name: Optional[str] = Field(None, min_length=2, max_length=20, description='First name')
    age: Optional[int] = Field(None, ge=18, le=100)
    city: Optional[str] = Field(None, min_length=2, max_length=30, description='Your city')
