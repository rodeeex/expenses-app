"""
Роутер для управления пользователями
"""
from uuid import UUID

from fastapi import APIRouter, status, Query

from src.schemas.user import (
    UserCreate,
    UserUpdate,
    UserRead,
    UserDeleteResponse,
)
from src.schemas.expense import UserExpenseSummary

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=list[UserExpenseSummary],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех пользователей с суммами расходов",
    description="Возвращает список всех пользователей с суммами их расходов за последний месяц. "
                "Используется для главной страницы приложения.",
    responses={
        200: {
            "description": "Список пользователей с суммами расходов",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "user_id": "123e4567-e89b-12d3-a456-426614174000",
                            "username": "john_doe",
                            "total_amount": 15000.50,
                            "expense_count": 25
                        },
                        {
                            "user_id": "223e4567-e89b-12d3-a456-426614174001",
                            "username": "jane_smith",
                            "total_amount": 8500.00,
                            "expense_count": 15
                        }
                    ]
                }
            }
        }
    },
)
async def get_all_users_with_expenses(
    month: int | None = Query(
        None,
        ge=1,
        le=12,
        description="Месяц для расчета расходов (1-12). Если не указан, используется текущий месяц."
    ),
    year: int | None = Query(
        None,
        ge=2000,
        le=2100,
        description="Год для расчета расходов. Если не указан, используется текущий год."
    ),
) -> list[UserExpenseSummary]:
    """
    Получить список всех пользователей с суммами расходов
    
    Возвращает список всех пользователей в системе с информацией о:
    - Общей сумме расходов за указанный период (по умолчанию - последний месяц)
    - Количестве расходов за период
    
    Используется для отображения на главной странице приложения.
    
    **Параметры запроса:**
    - **month**: Месяц (1-12), по умолчанию - текущий месяц
    - **year**: Год, по умолчанию - текущий год
    """
    # TODO: Реализовать получение списка пользователей с суммами расходов
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

