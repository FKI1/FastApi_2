from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine, Base
from .routers import users, advertisements, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Проверка необходимых переменных окружения
    import os
    if not os.getenv("SECRET_KEY"):
        raise ValueError("SECRET_KEY environment variable is not set. Please set it before starting the application.")
    
    # Создание таблиц на старте
    Base.metadata.create_all(bind=engine)
    yield
    # Очистка на завершении
    pass

app = FastAPI(
    title="Advertisement API",
    description="REST API for advertisements with user authentication",
    version="1.0.0",
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
