from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        v = v.strip()
        if " " in v:
            raise ValueError("username не должен содержать пробелы")
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if v.strip() != v:
            raise ValueError("password не должен начинаться/заканчиваться пробелами")
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=32)
    password: Optional[str] = Field(None, min_length=6, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if " " in v:
            raise ValueError("username не должен содержать пробелы")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v.strip() != v:
            raise ValueError("password не должен начинаться/заканчиваться пробелами")
        return v


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


class UserDeleteResponse(BaseModel):
    id: UUID
    detail: str = "User deleted"
