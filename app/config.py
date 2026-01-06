from pydantic_settings import BaseSettings
from typing import Optional
import warnings


class Settings(BaseSettings):
    # Безопасное значение по умолчанию только для разработки
    SECRET_KEY: str = "development-secret-key-do-not-use-in-production"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 48
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Предупреждение если используется дефолтный SECRET_KEY
        if self.SECRET_KEY == "development-secret-key-do-not-use-in-production":
            warnings.warn(
                "⚠️  ВНИМАНИЕ: Используется дефолтный SECRET_KEY. "
                "Для продакшена установите SECRET_KEY в .env файле.",
                UserWarning
            )


settings = Settings()
