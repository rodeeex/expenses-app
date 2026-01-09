from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.dependencies import get_current_user_id
from src.schemas.expense import UserExpenseSummary
from src.schemas.user import UserCreate, UserDeleteResponse, UserRead, UserUpdate
from src.services import auth as auth_service
from src.services import user as user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=list[UserExpenseSummary],
    status_code=status.HTTP_200_OK,
    summary="Получить всех пользователей с расходами за последний месяц",
    description="Возвращает список всех пользователей и сумму их расходов за последние 30 дней. "
    "Используется для главной страницы.",
    responses={
        200: {
            "description": "Список пользователей с расходами",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "user_id": "123e4567-e89b-12d3-a456-426614174000",
                            "username": "john_doe",
                            "total_amount": 50000.00,
                            "expense_count": 150,
                        }
                    ]
                }
            },
        }
    },
)
async def list_users(db: AsyncSession = Depends(get_db)) -> list[UserExpenseSummary]:
    """
    Получить всех пользователей с расходами за последний месяц

    Публичный эндпоинт для главной страницы.
    Возвращает список всех зарегистрированных пользователей и сумму их расходов за последние 30 дней.
    """
    return await user_service.get_all_users_with_last_month_expenses(db)


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
                        "username": "john_doe",
                    }
                }
            },
        },
        401: {"description": "Не авторизован"},
    },
)
async def get_current_user_endpoint(
    current_user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """
    Получить текущего авторизованного пользователя

    Возвращает информацию о пользователе, который выполнил авторизацию.
    Используется для отображения информации на странице профиля.
    """
    user = await user_service.get_current_user(db, current_user_id)
    return UserRead.model_validate(user)


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
                        "username": "john_doe_updated",
                    }
                }
            },
        },
        401: {"description": "Не авторизован"},
        400: {"description": "Пользователь с таким username уже существует"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def update_current_user_endpoint(
    user_data: UserUpdate,
    current_user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """
    Обновить текущего авторизованного пользователя

    - **username**: Новое имя пользователя (опционально)
    - **password**: Новый пароль (опционально)

    Можно обновить только указанные поля. Если поле не указано, оно остается без изменений.
    Используется для изменения данных на странице профиля.
    """
    user = await user_service.update_user(
        db, current_user_id, current_user_id, user_data
    )
    return UserRead.model_validate(user)


@router.delete(
    "/{user_id}",
    response_model=UserDeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Удалить пользователя",
    description="Удаляет пользователя из системы. Все связанные расходы также будут удалены.",
    responses={
        200: {
            "description": "Пользователь успешно удален",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "detail": "Пользователь удалён",
                    }
                }
            },
        },
        404: {"description": "Пользователь не найден"},
    },
)
async def delete_user_endpoint(
    user_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> UserDeleteResponse:
    """
    Удалить пользователя

    - **user_id**: UUID пользователя

    Удаляет пользователя и все связанные с ним данные:
    - все расходы пользователя
    - все refresh-токены пользователя
    """
    await auth_service.revoke_all_user_tokens(db, current_user_id)
    await user_service.delete_user(db, user_id, current_user_id)
    return UserDeleteResponse(id=user_id, detail="Пользователь удалён")
