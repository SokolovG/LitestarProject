from litestar import get, Router
from models.user import User


@get()
async def get_users() -> list[User]:
    return [
        User(
            username='test_user',
            first_name='Ivan',
            age=20,
            city='Tokio'

        )
    ]

user_router = Router(
    path='/users',
    route_handlers=[get_users]
)