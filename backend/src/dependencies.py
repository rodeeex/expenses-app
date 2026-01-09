from __future__ import annotations

from uuid import UUID

from fastapi import Cookie, HTTPException, status
from jose import JWTError

from src.services.auth import verify_access_token


async def get_current_user_id(
    access_token: str | None = Cookie(None),
) -> UUID:
    """
    Получить ID текущего авторизованного пользователя из httponly-cookie

    Raises HTTPException 401: токен отсутствует или невалиден
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен отсутствует",
        )

    try:
        user_id = verify_access_token(access_token)
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный токен",
        )
