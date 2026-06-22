from fastapi import APIRouter, Response, Depends

from src.api.dependencies.dependencies import DBDep, CurrentUserDep, PermissionChecker
from src.exceptions.exceptions import (
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
    UserAlreadyExistsException,
    UserEmailAlreadyExistsHTTPException,
    EmailDeletedException,
    EmailDeletedHTTPException,
    ForbiddenException,
    ForbiddenHTTPException,
)
from src.schemas.users import UserRequestAdd, UserLogin, UserRequestUpdate
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация")
async def register_user(db: DBDep, data: UserRequestAdd):
    """
    Регистрация пользователя
    """
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"status": "ok"}


@router.post("/login", summary="Аутентификация")
async def login_user(db: DBDep, data: UserLogin, response: Response):
    """
    Авторизация
    """
    try:
        access_token = await AuthService(db).login_user(data, response)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except EmailDeletedException:
        raise EmailDeletedHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    return {"access_token": access_token}


@router.post("/logout", summary="Выйти из системы")
async def logout_user(db: DBDep, response: Response):
    """
    Удалить access_token
    """
    await AuthService(db).logout_user(response)
    return {"status": "ok"}


@router.patch("/user/{user_id}", summary="Изменить информацию")
async def update_user(
    db: DBDep,
    user_id: int,
    data: UserRequestUpdate,
    current_user: CurrentUserDep,
    permission_data=Depends(PermissionChecker("users")),
):
    """
    Изменение информации пользователя
    """
    await AuthService(db).check_user(user_id)
    try:
        await AuthService(db).check_owner_permission(
            element=permission_data["element"],
            permission=permission_data["permission"],
            user_id=user_id,
            current_user=current_user,
        )
    except ForbiddenException:
        raise ForbiddenHTTPException
    try:
        await AuthService(db).patch_user(user_id, data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"status": "ok"}


@router.delete("/user/{user_id}", summary="Удалить пользователя")
async def delete_user(
    db: DBDep,
    user_id: int,
    current_user: CurrentUserDep,
    permission_data=Depends(PermissionChecker("users")),
):
    """
    Мягко удаляет пользователя
    """
    await AuthService(db).check_user(user_id)
    try:
        await AuthService(db).check_owner_permission(
            element=permission_data["element"],
            permission=permission_data["permission"],
            user_id=user_id,
            current_user=current_user,
        )
    except ForbiddenException:
        raise ForbiddenHTTPException
    await AuthService(db).delete_user(user_id)
    return {"status": "ok"}
