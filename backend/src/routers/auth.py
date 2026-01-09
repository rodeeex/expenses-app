from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.dependencies import get_current_user_id
from src.schemas.auth import LoginRequest, LogoutResponse
from src.schemas.user import UserCreate, UserRead
from src.services import auth as auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Маршрут не найден"}},
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
                        "username": "vasya_pupkin",
                    }
                }
            },
        },
        400: {"description": "Некорректные данные (например, username уже существует)"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """
    Регистрация нового пользователя

    - **username**: имя пользователя (3-32 символа, без пробелов)
    - **password**: пароль (минимум 6 символов)

    Возвращает информацию о созданном пользователе без пароля.
    """
    user = await auth_service.register_user(db, user_data)
    return UserRead.model_validate(user)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Авторизация пользователя",
    description="Авторизует пользователя и устанавливает httponly cookies с токенами",
    responses={
        200: {
            "description": "Успешная авторизация",
            "content": {
                "application/json": {"example": {"detail": "Успешная авторизация"}}
            },
        },
        401: {"description": "Неверные учетные данные"},
    },
)
async def login(
    credentials: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """
    Авторизация пользователя

    - **username**: имя пользователя
    - **password**: пароль

    При успешной авторизации устанавливает httponly cookies:
    - **access_token**: JWT-токен для доступа к защищенным эндпоинтам (30 минут)
    - **refresh_token**: токен для обновления access_token (30 дней)
    """
    user = await auth_service.authenticate_user(
        db, credentials.username, credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные данные для входа",
        )

    access_token = auth_service.create_access_token(user.id)
    refresh_token = await auth_service.create_refresh_token(db, user.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=1800,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=2592000,
    )

    return {"detail": "Успешный вход"}


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    summary="Обновление access-токена",
    description="Обновляет access-токен, используя валидный refresh-токен из cookie",
    responses={
        200: {
            "description": "Токен успешно обновлен",
            "content": {"application/json": {"example": {"detail": "Токен обновлён"}}},
        },
        401: {"description": "Невалидный или истекший refresh-токен"},
    },
)
async def refresh_token(
    response: Response,
    refresh_token: str | None = Cookie(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Обновление access токена

    Использует refresh токен из httponly-кук для генерации нового access-токена.
    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh-токен не найден",
        )

    try:
        user_id = await auth_service.verify_refresh_token(db, refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или просроченный refresh-токен",
        )

    new_access_token = auth_service.create_access_token(user_id)

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=1800,
    )

    return {"detail": "Токен обновлён"}


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Выход из аккаунта",
    description="Выходит из аккаунта, отзывая все refresh-токены пользователя",
    responses={
        200: {
            "description": "Успешный выход из аккаунта",
            "content": {"application/json": {"example": {"detail": "Успешный выход"}}},
        },
        401: {"description": "Не авторизован"},
    },
)
async def logout(
    response: Response,
    current_user_id=Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> LogoutResponse:
    """
    Выход из аккаунта

    Отзывает все refresh-токены пользователя и удаляет cookies.
    После выхода пользователь должен будет авторизоваться заново.
    """
    await auth_service.revoke_all_user_tokens(db, current_user_id)

    response.delete_cookie("access_token", httponly=True, samesite="lax")
    response.delete_cookie("refresh_token", httponly=True, samesite="lax")

    return LogoutResponse(detail="Успешный выход")
