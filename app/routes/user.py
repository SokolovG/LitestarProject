from litestar import get, Router
from models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.exceptions import NotFoundException
from typing import List

@get()
async def get_users(session: AsyncSession) -> List[User]:
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return users

@get('/{user_id:int}')
async def get_user_by_id(user_id: int, session: AsyncSession):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)

    # Like get_object_or_404
    user = result.scalar_one_or_none()
    if user is None:
        raise NotFoundException(f'User with {user_id} not found.')

    return user



user_router = Router(
    path='/users',
    route_handlers=[get_users]
)