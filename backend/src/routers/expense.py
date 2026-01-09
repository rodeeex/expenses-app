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
    summary="Получить список расходов текущего пользователя",
    description="Возвращает расходы авторизованного пользователя с фильтрацией по категории, способу оплаты и диапазону дат.",
)
async def get_expenses(
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
    skip: int = Query(0, ge=0, description="Пропустить записи (пагинация)"),
    limit: int = Query(100, ge=1, le=1000, description="Максимум записей"),
    current_user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> list[ExpenseRead]:
    expenses = await expense_service.list_expenses(
        db=db,
        current_user_id=current_user_id,
        category=category,
        payment_method=payment_method,
        date_from=date_from,
        date_to=date_to,
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
                        "detail": "Расход успешно удален",
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
    return ExpenseDeleteResponse(id=expense_id, detail="Расход успешно удален")
