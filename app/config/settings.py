from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class for DB settings."""
    DB_HOST: str = 'localhost'
    DB_PORT: int = '5432'
    DB_USER: str = 'postgres'
    DB_PASS: str = 'postgres'
    DB_NAME: str = 'postgres'

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"


settings = Settings()