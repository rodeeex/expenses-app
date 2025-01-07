from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.expense import Expense
from src.schemas.expense import ExpenseCreate, ExpenseUpdate


async def create_expense(
    db: AsyncSession,
    payload: ExpenseCreate,
    current_user_id: UUID | None = None,
) -> Expense:
    """
    Создать расход.
    Если в payload нет user_id — подставим current_user_id (если он передан).
    """
    data = payload.model_dump()
    if data.get("user_id") is None and current_user_id is not None:
        data["user_id"] = current_user_id
    elif data.get("user_id") != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя создавать расход для другого пользователя",
        )

    expense = Expense(**data)
    db.add(expense)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректные данные для создания расхода",
        ) from e
    await db.refresh(expense)
    return expense


async def get_expense_by_id(db: AsyncSession, expense_id: UUID) -> Expense:
    stmt = select(Expense).where(Expense.id == expense_id)
    result = await db.execute(stmt)
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Расход не найден"
        )
    return expense


async def list_expenses(
    db: AsyncSession,
    current_user_id: UUID | None = None,
    user_id: UUID | None = None,
    category: Optional[ExpenseCategory] = None,
    payment_method: Optional[PaymentMethod] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Expense]:
    stmt = select(Expense)

    if current_user_id is not None:
        stmt = stmt.where(Expense.user_id == current_user_id)
    elif user_id is not None:
        stmt = stmt.where(Expense.user_id == user_id)

    if category is not None:
        stmt = stmt.where(Expense.category == category)
    if payment_method is not None:
        stmt = stmt.where(Expense.payment_method == payment_method)
    if date_from is not None:
        stmt = stmt.where(Expense.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(Expense.date <= date_to)

    if hasattr(Expense, "date"):
        stmt = stmt.order_by(Expense.date.desc())
    elif hasattr(Expense, "created_at"):
        stmt = stmt.order_by(Expense.created_at.desc())

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def update_expense(
    db: AsyncSession,
    expense_id: UUID,
    payload: ExpenseUpdate,
    current_user_id: UUID | None = None,
) -> Expense:
    """
    Обновить расход.
    Доступно только владельцу расхода.
    """
    expense = await get_expense_by_id(db, expense_id)

    if expense.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя редактировать чужой расход",
        )

    data = payload.model_dump(exclude_unset=True)
    if not data:
        return expense

    for field, value in data.items():
        setattr(expense, field, value)

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректные данные для обновления расхода",
        ) from e
    await db.refresh(expense)
    return expense


async def delete_expense(
    db: AsyncSession,
    expense_id: UUID,
    current_user_id: UUID | None = None,
) -> None:
    """
    Удалить расход.
    Доступно только владельцу расхода.
    """
    expense = await get_expense_by_id(db, expense_id)

    if expense.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя удалять чужой расход",
        )

    await db.delete(expense)
    await db.commit()
