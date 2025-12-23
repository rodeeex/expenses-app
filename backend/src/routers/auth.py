"""
Роутер для аутентификации и авторизации пользователей
"""
from fastapi import APIRouter, status

from src.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    LogoutResponse,
)
from src.schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
    description="Создает нового пользователя в системе. Возвращает информацию о созданном пользователе.",
    responses={
        201: {
            "description": "Пользователь успешно зарегистрирован",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "username": "john_doe"
                    }
                }
            }
        },
        400: {"description": "Некорректные данные (например, username уже существует)"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def register(user_data: UserCreate) -> UserRead:
    """
    Регистрация нового пользователя
    
    - **username**: Имя пользователя (3-32 символа, без пробелов)
    - **password**: Пароль (минимум 6 символов)
    
    Возвращает информацию о созданном пользователе без пароля.
    """
    # TODO: Реализовать регистрацию
    pass


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Авторизация пользователя",
    description="Авторизует пользователя и возвращает пару токенов: access_token и refresh_token.",
    responses={
        200: {
            "description": "Успешная авторизация",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh_token": "refresh_token_string_here",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {"description": "Неверные учетные данные"},
        404: {"description": "Пользователь не найден"},
    },
)
async def login(credentials: LoginRequest) -> TokenResponse:
    """
    Авторизация пользователя
    
    - **username**: Имя пользователя
    - **password**: Пароль
    
    При успешной авторизации возвращает:
    - **access_token**: JWT токен для доступа к защищенным эндпоинтам
    - **refresh_token**: Токен для обновления access_token
    - **token_type**: Тип токена (обычно "bearer")
    
    Access токен имеет ограниченный срок действия, refresh токен используется для его обновления.
    """
    # TODO: Реализовать авторизацию
    pass


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновление access токена",
    description="Обновляет access токен используя валидный refresh токен.",
    responses={
        200: {
            "description": "Токен успешно обновлен",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh_token": "new_refresh_token_string_here",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {"description": "Невалидный или истекший refresh токен"},
        404: {"description": "Refresh токен не найден"},
    },
)
async def refresh_token(refresh_data: RefreshTokenRequest) -> TokenResponse:
    """
    Обновление access токена
    
    - **refresh_token**: Валидный refresh токен
    
    Возвращает новую пару токенов (access_token и refresh_token).
    Старый refresh токен может быть отозван в зависимости от стратегии безопасности.
    """
    # TODO: Реализовать обновление токена
    pass


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Выход из аккаунта",
    description="Выходит из аккаунта, отзывая текущий refresh токен.",
    responses={
        200: {
            "description": "Успешный выход из аккаунта",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Successfully logged out"
                    }
                }
            }
        },
        401: {"description": "Не авторизован"},
    },
)
async def logout(refresh_data: RefreshTokenRequest) -> LogoutResponse:
    """
    Выход из аккаунта
    
    - **refresh_token**: Refresh токен, который нужно отозвать
    
    Отзывает указанный refresh токен, делая его недействительным.
    После выхода пользователь должен будет авторизоваться заново для получения новых токенов.
    """
    # TODO: Реализовать выход из аккаунта
    pass

