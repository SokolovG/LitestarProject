from litestar import Litestar
from routes.user import user_router
import uvicorn

app = Litestar(route_handlers=[user_router])


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)