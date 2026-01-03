from __future__ import annotations

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """Ответ с токенами доступа"""

    access_token: str = Field(..., description="JWT токен доступа")
    refresh_token: str = Field(
        ..., description="Refresh токен для обновления access токена"
    )
    token_type: str = Field(default="bearer", description="Тип токена")


class LoginRequest(BaseModel):
    """Запрос на авторизацию"""

    username: str = Field(
        ..., min_length=3, max_length=32, description="Имя пользователя"
    )
    password: str = Field(..., min_length=6, max_length=128, description="Пароль")


class RefreshTokenRequest(BaseModel):
    """Запрос на обновление токена"""

    refresh_token: str = Field(..., description="Refresh токен для обновления")


class LogoutResponse(BaseModel):
    """Ответ на выход из аккаунта"""

    detail: str = Field(
        default="Successfully logged out", description="Сообщение об успешном выходе"
    )
