from __future__ import annotations

import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.models.enums import ExpenseCategory, PaymentMethod


class ExpenseBase(BaseModel):
    category: ExpenseCategory
    payment_method: PaymentMethod
    amount: float
    date: Optional[datetime.date] = None
    comment: Optional[str] = None

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            try:
                return datetime.date.fromisoformat(v)
            except ValueError:
                try:
                    d, m, y = map(int, v.split("."))
                    return datetime.date(y, m, d)
                except ValueError:
                    raise ValueError(
                        "Дата должна быть в формате YYYY-MM-DD или DD.MM.YYYY"
                    )
        raise ValueError("Неверный тип даты")

    @field_validator("comment")
    @classmethod
    def normalize_comment(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        return v or None


class ExpenseCreate(ExpenseBase):
    user_id: UUID


class ExpenseUpdate(BaseModel):
    category: Optional[ExpenseCategory] = None
    payment_method: Optional[PaymentMethod] = None
    amount: Optional[float] = Field(None, gt=0, le=1_000_000)
    date: Optional[datetime.date] = None
    comment: Optional[str] = Field(None, max_length=500)

    @field_validator("comment")
    @classmethod
    def normalize_comment(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        return v or None


class ExpenseRead(ExpenseBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID


class ExpenseDeleteResponse(BaseModel):
    id: UUID
    detail: str = "Расход удалён"


class ExpenseFilterParams(BaseModel):
    """
    Параметры фильтрации расходов
    """

    user_id: Optional[UUID] = Field(None, description="Фильтр по ID пользователя")
    category: Optional[ExpenseCategory] = Field(None, description="Фильтр по категории")
    payment_method: Optional[PaymentMethod] = Field(
        None, description="Фильтр по способу оплаты"
    )
    date_from: Optional[datetime.date] = Field(
        None, description="Начальная дата (включительно)"
    )
    date_to: Optional[datetime.date] = Field(
        None, description="Конечная дата (включительно)"
    )


class ExpenseStatisticsResponse(BaseModel):
    """
    Статистика по расходам
    """

    total_amount: float = Field(..., description="Общая сумма расходов")
    count: int = Field(..., description="Количество расходов")
    period_start: Optional[datetime.date] = Field(None, description="Начало периода")
    period_end: Optional[datetime.date] = Field(None, description="Конец периода")
    by_category: dict[str, float] = Field(
        default_factory=dict, description="Сумма по категориям"
    )
    by_payment_method: dict[str, float] = Field(
        default_factory=dict, description="Сумма по способам оплаты"
    )


class UserExpenseSummary(BaseModel):
    """
    Сводка расходов пользователя за определённый период
    """

    user_id: UUID
    username: str
    total_amount: float = Field(..., description="Общая сумма расходов за период")
    expense_count: int = Field(..., description="Количество расходов за период")
