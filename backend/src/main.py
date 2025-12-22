from fastapi import FastAPI

from src.routers import auth, user, expense

app = FastAPI(
    title="Expenses API",
    description="API для учета личных расходов",
    version="1.0.0",
)

# Подключение роутеров
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(expense.router)


@app.get("/health")
async def health():
    """Проверка работоспособности API"""
    return {"status": "ok"}
