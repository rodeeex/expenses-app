"""
Роутер для управления расходами
"""
from uuid import UUID
from datetime import date

from fastapi import APIRouter, status, Query

from src.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseRead,
    ExpenseDeleteResponse,
    ExpenseFilterParams,
    ExpenseStatisticsResponse,
)
from src.models.enums import ExpenseCategory, PaymentMethod

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=list[ExpenseRead],
    status_code=status.HTTP_200_OK,
    summary="Получить список расходов",
    description="Возвращает список расходов с возможностью фильтрации по различным параметрам.",
    responses={
        200: {
            "description": "Список расходов",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "user_id": "223e4567-e89b-12d3-a456-426614174001",
                            "category": "food",
                            "payment_method": "card",
                            "amount": 1500.50,
                            "date": "2024-12-22",
                            "comment": "Обед в ресторане"
                        }
                    ]
                }
            }
        }
    },
)
async def get_expenses(
    user_id: UUID | None = Query(None, description="Фильтр по ID пользователя"),
    category: ExpenseCategory | None = Query(None, description="Фильтр по категории"),
    payment_method: PaymentMethod | None = Query(None, description="Фильтр по способу оплаты"),
    date_from: date | None = Query(None, description="Начальная дата (включительно)"),
    date_to: date | None = Query(None, description="Конечная дата (включительно)"),
    skip: int = Query(0, ge=0, description="Количество записей для пропуска (пагинация)"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
) -> list[ExpenseRead]:
    """
    Получить список расходов с фильтрацией
    
    Возвращает список расходов с возможностью фильтрации по:
    - **user_id**: ID пользователя
    - **category**: Категория расхода
    - **payment_method**: Способ оплаты
    - **date_from**: Начальная дата периода (включительно)
    - **date_to**: Конечная дата периода (включительно)
    
    Поддерживает пагинацию:
    - **skip**: Количество записей для пропуска
    - **limit**: Максимальное количество записей в ответе (максимум 1000)
    
    Все фильтры опциональны и могут комбинироваться.
    """
    # TODO: Реализовать получение списка расходов с фильтрацией
    pass


@router.get(
    "/{expense_id}",
    response_model=ExpenseRead,
    status_code=status.HTTP_200_OK,
    summary="Получить расход по ID",
    description="Возвращает информацию о конкретном расходе по его идентификатору.",
    responses={
        200: {
            "description": "Информация о расходе",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "user_id": "223e4567-e89b-12d3-a456-426614174001",
                        "category": "food",
                        "payment_method": "card",
                        "amount": 1500.50,
                        "date": "2024-12-22",
                        "comment": "Обед в ресторане"
                    }
                }
            }
        },
        404: {"description": "Расход не найден"},
    },
)
async def get_expense(expense_id: UUID) -> ExpenseRead:
    """
    Получить расход по ID
    
    - **expense_id**: UUID расхода
    
    Возвращает полную информацию о расходе:
    - Категория
    - Сумма
    - Дата
    - Комментарий
    - Способ оплаты
    - ID пользователя
    """
    # TODO: Реализовать получение расхода
    pass


@router.post(
    "/",
    response_model=ExpenseRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый расход",
    description="Создает новую запись о расходе в системе.",
    responses={
        201: {
            "description": "Расход успешно создан",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "user_id": "223e4567-e89b-12d3-a456-426614174001",
                        "category": "food",
                        "payment_method": "card",
                        "amount": 1500.50,
                        "date": "2024-12-22",
                        "comment": "Обед в ресторане"
                    }
                }
            }
        },
        400: {"description": "Некорректные данные (например, пользователь не найден)"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def create_expense(expense_data: ExpenseCreate) -> ExpenseRead:
    """
    Создать новый расход
    
    - **user_id**: UUID пользователя, которому принадлежит расход
    - **category**: Категория расхода (food, transport, subscriptions, health, entertainment, utilities, other)
    - **payment_method**: Способ оплаты (cash, card, other)
    - **amount**: Сумма расхода (больше 0, максимум 1,000,000)
    - **date**: Дата расхода
    - **comment**: Комментарий (опционально, максимум 500 символов)
    
    Возвращает созданный расход с присвоенным ID.
    """
    # TODO: Реализовать создание расхода
    pass


@router.put(
    "/{expense_id}",
    response_model=ExpenseRead,
    status_code=status.HTTP_200_OK,
    summary="Обновить расход",
    description="Обновляет информацию о расходе. Можно обновить любое поле частично.",
    responses={
        200: {
            "description": "Расход успешно обновлен",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "user_id": "223e4567-e89b-12d3-a456-426614174001",
                        "category": "food",
                        "payment_method": "cash",
                        "amount": 2000.00,
                        "date": "2024-12-22",
                        "comment": "Обновленный комментарий"
                    }
                }
            }
        },
        404: {"description": "Расход не найден"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def update_expense(expense_id: UUID, expense_data: ExpenseUpdate) -> ExpenseRead:
    """
    Обновить расход
    
    - **expense_id**: UUID расхода
    - **category**: Новая категория (опционально)
    - **payment_method**: Новый способ оплаты (опционально)
    - **amount**: Новая сумма (опционально)
    - **date**: Новая дата (опционально)
    - **comment**: Новый комментарий (опционально)
    
    Можно обновить только указанные поля. Если поле не указано, оно остается без изменений.
    """
    # TODO: Реализовать обновление расхода
    pass


@router.delete(
    "/{expense_id}",
    response_model=ExpenseDeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Удалить расход",
    description="Удаляет расход из системы.",
    responses={
        200: {
            "description": "Расход успешно удален",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "detail": "Expense deleted"
                    }
                }
            }
        },
        404: {"description": "Расход не найден"},
    },
)
async def delete_expense(expense_id: UUID) -> ExpenseDeleteResponse:
    """
    Удалить расход
    
    - **expense_id**: UUID расхода
    
    Удаляет расход из системы.
    
    **Внимание:** Операция необратима!
    """
    # TODO: Реализовать удаление расхода
    pass


@router.get(
    "/statistics/summary",
    response_model=ExpenseStatisticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить статистику по расходам",
    description="Возвращает статистику по расходам с возможностью фильтрации по пользователю и периоду.",
    responses={
        200: {
            "description": "Статистика по расходам",
            "content": {
                "application/json": {
                    "example": {
                        "total_amount": 50000.00,
                        "count": 150,
                        "period_start": "2024-12-01",
                        "period_end": "2024-12-31",
                        "by_category": {
                            "food": 20000.00,
                            "transport": 15000.00,
                            "subscriptions": 5000.00,
                            "health": 3000.00,
                            "entertainment": 4000.00,
                            "utilities": 2000.00,
                            "other": 1000.00
                        },
                        "by_payment_method": {
                            "card": 40000.00,
                            "cash": 8000.00,
                            "other": 2000.00
                        }
                    }
                }
            }
        }
    },
)
async def get_expense_statistics(
    user_id: UUID | None = Query(None, description="ID пользователя для фильтрации статистики"),
    date_from: date | None = Query(None, description="Начальная дата периода (включительно)"),
    date_to: date | None = Query(None, description="Конечная дата периода (включительно)"),
    month: int | None = Query(
        None,
        ge=1,
        le=12,
        description="Месяц для расчета статистики (1-12). Если указан, используется текущий год."
    ),
    year: int | None = Query(
        None,
        ge=2000,
        le=2100,
        description="Год для расчета статистики. Если указан только год, возвращается статистика за весь год."
    ),
) -> ExpenseStatisticsResponse:
    """
    Получить статистику по расходам
    
    Возвращает агрегированную статистику по расходам:
    - **total_amount**: Общая сумма расходов
    - **count**: Количество расходов
    - **period_start/period_end**: Период расчета
    - **by_category**: Сумма расходов по каждой категории
    - **by_payment_method**: Сумма расходов по каждому способу оплаты
    
    **Параметры фильтрации:**
    - **user_id**: Фильтр по пользователю (опционально)
    - **date_from/date_to**: Период в виде диапазона дат
    - **month/year**: Период в виде месяца и года (если указан только year - весь год)
    
    Если не указан период, возвращается статистика за текущий месяц.
    """
    # TODO: Реализовать получение статистики
    pass

