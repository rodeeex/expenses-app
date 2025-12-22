from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator

from src.models.enums import ExpenseCategory, PaymentMethod


class ExpenseBase(BaseModel):
    category: ExpenseCategory
    payment_method: PaymentMethod
    amount: float = Field(..., gt=0, le=1_000_000)
    date: date
    comment: str | None = Field(None, max_length=500)

    @field_validator("comment")
    @classmethod
    def normalize_comment(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        return v or None


class ExpenseCreate(ExpenseBase):
    user_id: UUID


class ExpenseUpdate(BaseModel):
    category: ExpenseCategory | None = None
    payment_method: PaymentMethod | None = None
    amount: float | None = Field(None, gt=0, le=1_000_000)
    date: date | None = None
    comment: str | None = Field(None, max_length=500)

    @field_validator("comment")
    @classmethod
    def normalize_comment(cls, v: str | None) -> str | None:
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
    detail: str = "Expense deleted"


class ExpenseFilterParams(BaseModel):
    """Параметры фильтрации расходов"""
    user_id: UUID | None = Field(None, description="Фильтр по ID пользователя")
    category: ExpenseCategory | None = Field(None, description="Фильтр по категории")
    payment_method: PaymentMethod | None = Field(None, description="Фильтр по способу оплаты")
    date_from: date | None = Field(None, description="Начальная дата (включительно)")
    date_to: date | None = Field(None, description="Конечная дата (включительно)")


class ExpenseStatisticsResponse(BaseModel):
    """Статистика по расходам"""
    total_amount: float = Field(..., description="Общая сумма расходов")
    count: int = Field(..., description="Количество расходов")
    period_start: date | None = Field(None, description="Начало периода")
    period_end: date | None = Field(None, description="Конец периода")
    by_category: dict[str, float] = Field(default_factory=dict, description="Сумма по категориям")
    by_payment_method: dict[str, float] = Field(default_factory=dict, description="Сумма по способам оплаты")


class UserExpenseSummary(BaseModel):
    """Сводка расходов пользователя за период"""
    user_id: UUID
    username: str
    total_amount: float = Field(..., description="Общая сумма расходов за период")
    expense_count: int = Field(..., description="Количество расходов за период")
