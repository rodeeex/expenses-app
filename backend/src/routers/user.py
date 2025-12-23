"""
Роутер для управления пользователями
"""
from uuid import UUID

from fastapi import APIRouter, status

from src.schemas.user import (
    UserCreate,
    UserUpdate,
    UserRead,
    UserDeleteResponse,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Получить текущего авторизованного пользователя",
    description="Возвращает информацию о текущем авторизованном пользователе. "
                "Используется для страницы профиля.",
    responses={
        200: {
            "description": "Информация о текущем пользователе",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "username": "john_doe"
                    }
                }
            }
        },
        401: {"description": "Не авторизован"},
    },
)
async def get_current_user() -> UserRead:
    """
    Получить текущего авторизованного пользователя
    
    Возвращает информацию о пользователе, который выполнил авторизацию.
    Требует валидный access токен в заголовке Authorization.
    
    Используется для отображения информации на странице профиля.
    """
    # TODO: Реализовать получение текущего пользователя
    pass


@router.put(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Обновить текущего авторизованного пользователя",
    description="Обновляет информацию о текущем авторизованном пользователе. "
                "Можно обновить username и/или password. Используется для страницы профиля.",
    responses={
        200: {
            "description": "Пользователь успешно обновлен",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "username": "john_doe_updated"
                    }
                }
            }
        },
        401: {"description": "Не авторизован"},
        400: {"description": "Пользователь с таким username уже существует"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def update_current_user(user_data: UserUpdate) -> UserRead:
    """
    Обновить текущего авторизованного пользователя
    
    - **username**: Новое имя пользователя (опционально)
    - **password**: Новый пароль (опционально)
    
    Можно обновить только указанные поля. Если поле не указано, оно остается без изменений.
    Требует валидный access токен в заголовке Authorization.
    
    Используется для изменения данных на странице профиля.
    """
    # TODO: Реализовать обновление текущего пользователя
    pass


@router.get(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Получить пользователя по ID",
    description="Возвращает информацию о пользователе по его идентификатору.",
    responses={
        200: {
            "description": "Информация о пользователе",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "username": "john_doe"
                    }
                }
            }
        },
        404: {"description": "Пользователь не найден"},
    },
)
async def get_user(user_id: UUID) -> UserRead:
    """
    Получить пользователя по ID
    
    - **user_id**: UUID пользователя
    
    Возвращает базовую информацию о пользователе (без пароля).
    """
    # TODO: Реализовать получение пользователя
    pass


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового пользователя",
    description="Создает нового пользователя в системе. "
                "Для регистрации рекомендуется использовать /auth/register.",
    responses={
        201: {
            "description": "Пользователь успешно создан",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "username": "john_doe"
                    }
                }
            }
        },
        400: {"description": "Пользователь с таким username уже существует"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def create_user(user_data: UserCreate) -> UserRead:
    """
    Создать нового пользователя
    
    - **username**: Имя пользователя (3-32 символа, без пробелов)
    - **password**: Пароль (минимум 6 символов)
    
    Для регистрации пользователей рекомендуется использовать эндпоинт `/auth/register`,
    который также выполняет необходимые проверки и создание токенов.
    """
    # TODO: Реализовать создание пользователя
    pass


@router.put(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Обновить пользователя",
    description="Обновляет информацию о пользователе. Можно обновить username и/или password.",
    responses={
        200: {
            "description": "Пользователь успешно обновлен",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "username": "john_doe_updated"
                    }
                }
            }
        },
        404: {"description": "Пользователь не найден"},
        400: {"description": "Пользователь с таким username уже существует"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def update_user(user_id: UUID, user_data: UserUpdate) -> UserRead:
    """
    Обновить пользователя
    
    - **user_id**: UUID пользователя
    - **username**: Новое имя пользователя (опционально)
    - **password**: Новый пароль (опционально)
    
    Можно обновить только указанные поля. Если поле не указано, оно остается без изменений.
    """
    # TODO: Реализовать обновление пользователя
    pass


@router.delete(
    "/{user_id}",
    response_model=UserDeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Удалить пользователя",
    description="Удаляет пользователя из системы. Все связанные расходы также будут удалены (CASCADE).",
    responses={
        200: {
            "description": "Пользователь успешно удален",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "detail": "User deleted"
                    }
                }
            }
        },
        404: {"description": "Пользователь не найден"},
    },
)
async def delete_user(user_id: UUID) -> UserDeleteResponse:
    """
    Удалить пользователя
    
    - **user_id**: UUID пользователя
    
    Удаляет пользователя и все связанные с ним данные:
    - Все расходы пользователя (CASCADE удаление)
    - Все refresh токены пользователя
    
    """
    # TODO: Реализовать удаление пользователя
    pass

