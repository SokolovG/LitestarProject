from sqlalchemy import Column, Integer, String
from database.connection import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100))

    def __repr__(self):
        return f'<User {self.username}>'