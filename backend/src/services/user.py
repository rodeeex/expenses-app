from __future__ import annotations

from datetime import datetime, timedelta
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.expense import Expense
from src.models.user import User
from src.schemas.expense import UserExpenseSummary
from src.schemas.user import UserUpdate
from src.services.auth import hash_password


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> User:
    """
    Получить пользователя по ID
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user


async def get_current_user(db: AsyncSession, current_user_id: UUID) -> User:
    """
    Получить текущего пользователя
    """
    stmt = select(User).where(User.id == current_user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user


async def get_all_users_with_last_month_expenses(
    db: AsyncSession,
) -> list[UserExpenseSummary]:
    """
    Получить всех пользователей с суммой расходов за последний месяц (для главной страницы)
    """
    month_ago = (datetime.utcnow() - timedelta(days=30)).date()

    stmt = (
        select(
            User.id,
            User.username,
            func.coalesce(func.sum(Expense.amount), 0).label("total_amount"),
            func.count(Expense.id).label("expense_count"),
        )
        .outerjoin(
            Expense,
            (Expense.user_id == User.id) & (Expense.date >= month_ago),
        )
        .group_by(User.id, User.username)
    )

    result = await db.execute(stmt)

    return [
        UserExpenseSummary(
            user_id=row.id,
            username=row.username,
            total_amount=float(row.total_amount),
            expense_count=row.expense_count,
        )
        for row in result.all()
    ]


async def update_user(
    db: AsyncSession,
    user_id: UUID,
    current_user_id: UUID,
    user_data: UserUpdate,
) -> User:
    """
    Обновить пользователя
    """
    if user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    update_data = user_data.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))
    for field, value in update_data.items():
        setattr(user, field, value)
    try:
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким никнеймом уже существует",
        )


async def delete_user(db: AsyncSession, user_id: UUID, current_user_id: UUID) -> None:
    """
    Удалить аккаунт
    """
    if user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    await db.delete(user)
    await db.commit()
