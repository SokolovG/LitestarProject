from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from litestar import Router, delete, get, post, put
from litestar.exceptions import NotFoundException

from config.exceptions import UserAlreadyExistError
from models.user import User
from schemas.user import UpdateUserSchema, UserSchema


@get()
async def get_users(session: AsyncSession) -> List[UserSchema]:
    """Get all users."""
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return [UserSchema.from_orm(user) for user in users]

@get('/{user_id:int}')
async def get_user_by_id(user_id: int, session: AsyncSession) -> dict:
    """Get user by id."""
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)

    # Like get_object_or_404
    user = result.scalar_one_or_none()
    if user is None:
        raise NotFoundException(f'User with {user_id} not found.')

    return {"id": user.id, "username": user.username, "email": user.email}


@put('/update/{user_id:int}')
async def update_user(user_id: int, data: UpdateUserSchema, session: AsyncSession) -> dict:
    """Update user data."""
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise NotFoundException(f'User with {user_id} not found.')

    if user.username != data.username:
        existing_user_query = select(User).where(User.username == data.username)
        exist_user = await session.execute(existing_user_query)
        if exist_user.scalar_one_or_none():
            raise UserAlreadyExistError()

    user.username = data.username
    user.email = data.email
    await session.commit()
    await session.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email}


@post('/create')
async def create_user(data: UserSchema, session: AsyncSession) -> dict:
    """Create user."""
    query = select(User).where(User.username == data.username)
    existing_user = await session.execute(query)

    if existing_user.scalar_one_or_none():
        raise UserAlreadyExistError()
    user = User(
        username=data.username,
        email=data.email
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email}


@delete('/delete/{user_id:int}')
async def delete_user(user_id: int, session: AsyncSession) -> None:
    """Delete user."""
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise NotFoundException(f'User with {user_id} not found.')

    await session.delete(user)
    await  session.commit()


user_router = Router(
    path='/users',
    route_handlers=[get_users, get_user_by_id, create_user, update_user, delete_user]
)