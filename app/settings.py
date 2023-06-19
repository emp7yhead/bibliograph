from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    app_name: str = 'bibliograph'
    description: str = 'App for organizing book collections'
    version: str = "0.0.1"
    contact: dict = {
        'name': 'Artyom Kropp',
        'email': 'artyomkropp@gmail.com',
    }
    tags_metadata: list = [
        {
            "name": "Users",
            "description": "Operations with users.",
        },
        {
            "name": "Auth",
            "description": "Login and registration.",
        },
        {
            "name": "Books",
            "description": "Operations with user books.",
        },
        {
            "name": "Bookshelves",
            "description": "Managing user's bookshelves.",
        },
    ]
    SECRET_KEY: str = 'very secret key'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: Optional[str]
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str],
        values: Dict[str, Any],
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = './.env'


settings = Settings()
