from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine, Base
from .routers import users, advertisements, auth
import warnings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Предупреждение если используется дефолтный SECRET_KEY
    from .config import settings
    if settings.SECRET_KEY == "development-secret-key-do-not-use-in-production":
        warnings.warn(
            "⚠️  ВНИМАНИЕ: Используется дефолтный SECRET_KEY. "
            "Для продакшена установите SECRET_KEY в .env файле.",
            UserWarning
        )
    
    # Создание таблиц на старте
    Base.metadata.create_all(bind=engine)
    yield
    # Очистка на завершении
    pass

app = FastAPI(
    title="Advertisement API",
    description="REST API for advertisements with user authentication",
    version="2.0.0",
    lifespan=lifespan
)

# Подключение роутеров
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(advertisements.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Advertisement API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}