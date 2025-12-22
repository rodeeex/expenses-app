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
