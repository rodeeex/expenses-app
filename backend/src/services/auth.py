from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models.refresh_token import RefreshToken
from src.models.user import User
from src.schemas.user import UserCreate

# Argon2 хешер
ph = PasswordHasher()


# Пароли
def hash_password(password: str) -> str:
    """
    Хеширование пароля через Argon2
    """
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля через Argon2
    """
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False


# Access-токены
def create_access_token(user_id: UUID) -> str:
    """
    Создание access-токена
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"user_id": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.KEY_DEFAULT, algorithm="HS256")


def verify_access_token(token: str) -> UUID:
    """
    Проверка access-токена и извлечение user_id
    """
    payload = jwt.decode(token, settings.KEY_DEFAULT, algorithms=["HS256"])
    return UUID(payload["user_id"])


# Refresh-токены
async def create_refresh_token(
    db: AsyncSession,
    user_id: UUID,
    user_agent: str | None = None,
    ip: str | None = None,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload = {"user_id": str(user_id), "exp": expire}
    token = jwt.encode(payload, settings.KEY_DEFAULT, algorithm="HS256")

    token_hash = hashlib.sha256(token.encode()).hexdigest()

    db_token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expire.replace(tzinfo=None),
        user_agent=user_agent,
        ip=ip,
    )
    db.add(db_token)
    await db.commit()
    return token


async def verify_refresh_token(db: AsyncSession, token: str) -> UUID:
    payload = jwt.decode(token, settings.KEY_DEFAULT, algorithms=["HS256"])
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    stmt = select(RefreshToken).where(
        RefreshToken.token_hash == token_hash,
        RefreshToken.revoked_at.is_(None),
    )
    result = await db.execute(stmt)
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now(timezone.utc).replace(
        tzinfo=None
    ):
        raise JWTError("Неверный или просроченный refresh-токен")

    return UUID(payload["user_id"])


async def revoke_refresh_token(db: AsyncSession, token: str) -> None:
    """
    Отзыв конкретного refresh токена
    """
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    result = await db.execute(stmt)
    db_token = result.scalar_one_or_none()

    if db_token:
        db_token.revoked_at = datetime.now(timezone.utc)
        await db.commit()


async def revoke_all_user_tokens(db: AsyncSession, user_id: UUID) -> None:
    """
    Отзыв всех refresh токенов пользователя
    """
    stmt = select(RefreshToken).where(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked_at.is_(None),
    )
    result = await db.execute(stmt)
    tokens = result.scalars().all()

    for token in tokens:
        token.revoked_at = datetime.now(timezone.utc)

    await db.commit()


# Вход + регистрация
async def register_user(db: AsyncSession, user_data: UserCreate) -> User:
    """
    Регистрация нового пользователя
    """
    hashed_password = hash_password(user_data.password)

    db_user = User(username=user_data.username, password_hash=hashed_password)
    db.add(db_user)

    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким никнеймом уже существует",
        )


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> User | None:
    """
    Аутентификация пользователя
    """
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        return None
    return user
