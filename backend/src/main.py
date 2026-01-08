import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth, expense, user

app = FastAPI(
    title="Expenses API",
    description="API для учета личных расходов",
    version="1.0.0",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Подключение роутеров
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(expense.router)


@app.get("/health")
async def health():
    """Проверка работоспособности API"""
    return {"status": "ok"}
