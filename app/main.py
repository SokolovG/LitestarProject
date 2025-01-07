from litestar import Litestar
from routes.user import user_router
from database.connection import engine, Base, get_session
import uvicorn


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = Litestar(route_handlers=[user_router],
               on_startup=[create_tables],
               dependencies={"session": get_session},
               debug=True
               )


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)