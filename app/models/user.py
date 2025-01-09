from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from pydantic import ConfigDict
from passlib.context import CryptContext
from sqlalchemy.orm import relationship
from datetime import datetime

from database.connection import Base


pwd_context = CryptContext(schemes=['bcrypt'])


class User(Base):
    """Class for standard user model."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        str_strip_whitespace=True
    )
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), index=True, nullable=False)
    first_name = Column(String(30))
    last_name = Column(String(30))
    hashed_password = Column(String, nullable=False)
    sessions = relationship('Session', back_populates="user", cascade="all, delete")


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, plain_password: str):
        self.hashed_password = pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)

    def __repr__(self):
        return f'<User {self.username}>'


class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    user = relationship('User', back_populates='sessions')

    def __repr__(self):
        return f'<Session {self.id} for user {self.user_id}>'