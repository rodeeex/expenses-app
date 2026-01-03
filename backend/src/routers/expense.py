"""
Роутер для управления расходами
"""

from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.dependencies import get_current_user_id
from src.models.enums import ExpenseCategory, PaymentMethod
from src.schemas.expense import (
    ExpenseCreate,
    ExpenseDeleteResponse,
    ExpenseRead,
    ExpenseStatisticsResponse,
    ExpenseUpdate,
)
from src.services import expense as expense_service

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
                            "comment": "Обед в ресторане",
                        }
                    ]
                }
            },
        }
    },
)
async def get_expenses(
    user_id: Optional[UUID] = Query(None, description="Фильтр по ID пользователя"),
    category: Optional[ExpenseCategory] = Query(
        None, description="Фильтр по категории"
    ),
    payment_method: Optional[PaymentMethod] = Query(
        None, description="Фильтр по способу оплаты"
    ),
    date_from: Optional[date] = Query(
        None, description="Начальная дата (включительно)"
    ),
    date_to: Optional[date] = Query(None, description="Конечная дата (включительно)"),
    skip: int = Query(
        0, ge=0, description="Количество записей для пропуска (пагинация)"
    ),
    limit: int = Query(
        100, ge=1, le=1000, description="Максимальное количество записей"
    ),
    current_user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> list[ExpenseRead]:
    """
    Получить список расходов с фильтрацией

    Возвращает список расходов с возможностью фильтрации по различным параметрам.
    Пользователь может видеть только свои расходы.
    """
    expenses = await expense_service.list_expenses(
        db=db,
        user_id=current_user_id,
        skip=skip,
        limit=limit,
    )
    return [ExpenseRead.model_validate(exp) for exp in expenses]


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
                        "comment": "Обед в ресторане",
                    }
                }
            },
        },
        404: {"description": "Расход не найден"},
        403: {"description": "Нет доступа к этому расходу"},
    },
)
async def get_expense(
    expense_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> ExpenseRead:
    """
    Получить расход по ID

    Возвращает информацию о расходе. Пользователь может видеть только свои расходы.
    """
    expense = await expense_service.get_expense_by_id(db, expense_id)

    if expense.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому расходу",
        )

    return ExpenseRead.model_validate(expense)


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
                        "comment": "Обед в ресторане",
                    }
                }
            },
        },
        400: {"description": "Некорректные данные"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def create_expense(
    expense_data: ExpenseCreate,
    current_user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> ExpenseRead:
    """
    Создать новый расход

    Создаёт расход для текущего авторизованного пользователя.
    """
    expense = await expense_service.create_expense(
        db=db,
        payload=expense_data,
        current_user_id=current_user_id,
    )
    return ExpenseRead.model_validate(expense)


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
                        "comment": "Обновленный комментарий",
                    }
                }
            },
        },
        404: {"description": "Расход не найден"},
        403: {"description": "Нет доступа к этому расходу"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def update_expense(
    expense_id: UUID,
    expense_data: ExpenseUpdate,
    current_user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> ExpenseRead:
    """
    Обновить расход

    Обновляет расход. Пользователь может обновлять только свои расходы.
    """
    expense = await expense_service.get_expense_by_id(db, expense_id)
    if expense.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому расходу",
        )

    updated_expense = await expense_service.update_expense(
        db=db,
        expense_id=expense_id,
        payload=expense_data,
        current_user_id=current_user_id,
    )
    return ExpenseRead.model_validate(updated_expense)


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
                        "detail": "Expense deleted",
                    }
                }
            },
        },
        404: {"description": "Расход не найден"},
        403: {"description": "Нет доступа к этому расходу"},
    },
)
async def delete_expense(
    expense_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> ExpenseDeleteResponse:
    """
    Удалить расход

    Удаляет расход. Пользователь может удалять только свои расходы.
    """
    expense = await expense_service.get_expense_by_id(db, expense_id)
    if expense.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому расходу",
        )

    await expense_service.delete_expense(
        db=db,
        expense_id=expense_id,
        current_user_id=current_user_id,
    )
    return ExpenseDeleteResponse(id=expense_id, detail="Expense deleted")


@router.get(
    "/statistics/summary",
    response_model=ExpenseStatisticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить статистику по расходам",
    description="Возвращает статистику по расходам текущего пользователя.",
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
                        },
                        "by_payment_method": {
                            "card": 40000.00,
                            "cash": 8000.00,
                        },
                    }
                }
            },
        }
    },
)
async def get_expense_statistics(
    date_from: Optional[date] = Query(
        None, description="Начальная дата периода (включительно)"
    ),
    date_to: Optional[date] = Query(
        None, description="Конечная дата периода (включительно)"
    ),
    month: Optional[int] = Query(
        None,
        ge=1,
        le=12,
        description="Месяц для расчета статистики (1-12). Если указан, используется текущий год.",
    ),
    year: Optional[int] = Query(
        None, ge=2000, le=2100, description="Год для расчета статистики."
    ),
    current_user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> ExpenseStatisticsResponse:
    """
    Получить статистику по расходам

    Возвращает агрегированную статистику по расходам текущего пользователя.
    Если период не указан, возвращается статистика за текущий месяц.
    """
    # TODO: Реализовать получение статистики через expense_service
    # Пока заглушка
    return ExpenseStatisticsResponse(
        total_amount=0.0,
        count=0,
        period_start=date_from,
        period_end=date_to,
        by_category={},
        by_payment_method={},
    )
