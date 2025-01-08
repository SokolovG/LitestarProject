from sqlalchemy import Column, Integer, String
from pydantic import ConfigDict

from database.connection import Base


class User(Base):
    """Class for standart user model."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        str_strip_whitespace=True
    )
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    email = Column(String(100))

    def __repr__(self):
        return f'<User {self.username}>'