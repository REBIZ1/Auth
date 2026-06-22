from typing import Annotated

from fastapi import Depends, Request

from src.exceptions.exceptions import EmailDeletedHTTPException, ForbiddenHTTPException
from src.schemas.users import User
from src.services.auth import AuthService
from src.exceptions.exceptions import (
    NoAccessTokenHTTPException,
    IncorrectTokenException,
    IncorrectTokenHTTPException,
    ObjectNotFoundException,
    UserNotFoundHTTPException,
)
from src.core.database import async_session_maker
from src.core.db_manager import DBManager


async def get_db():
    """
    Создает асинхронную сессию базы данных через DBManager
    и автоматически закрывает её после завершения запроса

    yield:
        DBManager: Экземпляр менеджера базы данных
    """
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


def get_token(request: Request) -> str | None:
    """
    Извлекает access_token из cookies запроса
    """
    token = request.cookies.get("access_token")
    if not token:
        raise NoAccessTokenHTTPException
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    """
    Декодирует токен и возвращает id текущего пользователя
    """
    try:
        data = AuthService().decode_token(token)
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_current_user(db: DBDep, user_id: UserIdDep):
    """
    Получить текущего пользователя
    """
    try:
        user = await db.users.get_one(id=user_id)
    except ObjectNotFoundException:
        raise UserNotFoundHTTPException
    if not user.is_active:
        raise EmailDeletedHTTPException
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


class PermissionChecker:
    """
    Проверка прав
    """

    def __init__(self, element_name: str):
        self.element_name = element_name

    async def __call__(self, request: Request, db: DBDep, current_user: CurrentUserDep):
        permission_map = {
            "GET": "read_permission",
            "POST": "create_permission",
            "PATCH": "update_permission",
            "PUT": "update_permission",
            "DELETE": "delete_permission",
        }
        permission_name = permission_map.get(request.method)
        if not permission_name:
            raise ForbiddenHTTPException
        rule = await db.access_rule.get_rule(
            role_id=current_user.role_id,
            element_name=self.element_name,
        )
        allowed = getattr(rule, permission_name)
        if not allowed:
            raise ForbiddenHTTPException
        return {
            "element": self.element_name,
            "permission": permission_name,
        }
