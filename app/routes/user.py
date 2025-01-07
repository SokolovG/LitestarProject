from litestar import get, Router
from models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

@get()
async def get_users(session: AsyncSession) -> List[User]:
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


user_router = Router(
    path='/users',
    route_handlers=[get_users]
)