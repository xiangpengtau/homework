from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    REDIS_HOST: str
    REDIS_PORT: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"

# Initialize settings instance
settings = Settings()
