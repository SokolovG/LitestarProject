from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.settings import settings


# Creating engine.
engine = create_async_engine(
    url=settings.database_url,
    echo=True
)

# Creating parent class for models.
Base = declarative_base()


SessionFactory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with SessionFactory() as session:
        yield session