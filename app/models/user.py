from sqlalchemy import Column, Integer, String
from database.connection import Base
from pydantic import ConfigDict

class User(Base):
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