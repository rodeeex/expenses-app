from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Index, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import GUID, Base, TimestampMixin
from .enums import ExpenseCategory, PaymentMethod


class Expense(Base, TimestampMixin):
    __tablename__ = "expenses"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)

    category: Mapped[ExpenseCategory] = mapped_column(
        Enum(ExpenseCategory, native_enum=False),
        nullable=False,
        index=True,
    )

    # В БД колонка называется sum (как в ТЗ/схеме)
    amount: Mapped[float] = mapped_column("sum", Numeric(12, 2), nullable=False)

    date: Mapped[date] = mapped_column("date", Date, nullable=False, index=True)

    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod, native_enum=False),
        nullable=False,
        index=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(back_populates="expenses")


Index("ix_expenses_user_date", Expense.user_id, Expense.expense_date)
