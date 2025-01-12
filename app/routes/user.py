from typing import List

from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from litestar import delete, get, post, put, Controller
from litestar.exceptions import NotFoundException
from litestar import Litestar

from config.exceptions import UserAlreadyExistError, DatabaseError
from models.user import User
from schemas.user import UpdateUserSchema, UserSchema, UserCreateSchema


class UserController(Controller):
    path = '/users'

    @get()
    async def get_users(self, session: AsyncSession) -> List[UserSchema]:
        """Get all users."""
        query = select(User)
        result = await session.execute(query)
        users = result.scalars().all()
        return [UserSchema.from_orm(user) for user in users]

    @get('/{username:str}')
    async def get_user_by_username(self, username: str, session: AsyncSession) -> UserSchema:
        """Get user by username."""
        query = select(User).where(User.username == username)
        result = await session.execute(query)

        user = result.scalar_one_or_none()
        if user is None:
            raise NotFoundException(f'User with {username} not found.')

        return UserSchema.from_orm(user)

    @put('/update/{username:str}')
    async def update_user(self, username: str, data: UpdateUserSchema, session: AsyncSession) -> dict:
        """Update user data."""
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise NotFoundException(f'User with {username} not found.')

        if user.username != data.username:
            existing_user_query = (
                select(User).where(User.username == data.username))
            exist_user = await session.execute(existing_user_query)
            if exist_user.scalar_one_or_none():
                raise UserAlreadyExistError()

        user.username = data.username
        user.email = data.email
        await session.commit()
        await session.refresh(user)
        return UpdateUserSchema.from_orm(user)

    @delete('/delete/{username:str}')
    async def delete_user(self, username: str, session: AsyncSession) -> None:
        """Delete user."""
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise NotFoundException(f'User with {username} not found.')

        await session.delete(user)
        await session.commit()


class RegisterController(Controller):
    path = '/register'

    @post()
    async def create_user(self, data: UserCreateSchema, session: AsyncSession) -> dict:
        """Create user."""
        query = select(User).where(
            or_(
                User.username == data.username,
                User.email == data.email
            )
        )
        existing_user = await session.execute(query)

        if existing_user.scalar_one_or_none():
            raise UserAlreadyExistError()

        user = User(
            username=data.username,
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,

        )
        user.password = data.password
        try:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print(f"Debug: User ID after refresh: {user.id}")
            return UserCreateSchema.from_orm(user)

        except SQLAlchemyError as sql_error:
            await session.rollback()
            raise DatabaseError(str(sql_error))


