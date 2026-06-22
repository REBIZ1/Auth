from datetime import datetime, timezone, timedelta

import jwt
from fastapi import Response
from passlib.context import CryptContext
from sqlalchemy.exc import NoResultFound

from src.core.config import settings
from src.exceptions.exceptions import (
    ObjectAlreadyExistsException,
    IncorrectTokenException,
    EmailNotRegisteredException,
    IncorrectPasswordException,
    UserAlreadyExistsException,
    EmailDeletedException,
    ObjectNotFoundException,
    UserNotFoundHTTPException,
)
from src.schemas.users import (
    UserRequestAdd,
    UserAdd,
    UserLogin,
    UserUpdate,
    UserRequestUpdate,
)
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    async def check_user(self, user_id: int):
        """
        Проверить пользователя
        """
        try:
            await self.db.users.get_one(id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundHTTPException

    def create_access_token(self, data: dict):
        """
        Создать access_token
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        """
        Проверка пароля
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def hashed_password(self, password: str) -> str:
        """
        Хэширование пароля
        """
        return self.pwd_context.hash(password)

    def decode_token(self, token: str):
        """
        Декодирование токена
        """
        try:
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException

    async def register_user(self, data: UserRequestAdd):
        """
        Регистрация пользователя
        """
        hashed_password = self.hashed_password(data.password)
        new_user_data = UserAdd(
            first_name=data.first_name,
            middle_name=data.middle_name,
            last_name=data.last_name,
            email=data.email,
            hashed_password=hashed_password,
        )
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as e:
            raise UserAlreadyExistsException from e

    async def login_user(self, data: UserLogin, response: Response):
        """
        Авторизация
        """
        try:
            user = await self.db.users.get_user_with_hashed_password(email=data.email)
        except NoResultFound:
            raise EmailNotRegisteredException
        if not user.is_active:
            raise EmailDeletedException
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return access_token

    async def patch_user(self, user_id: int, data: UserRequestUpdate):
        """
        Частично изменяет информацию пользователя
        """
        update_data = data.model_dump(
            exclude_unset=True,
            exclude={"old_password", "new_password", "new_password2"},
        )
        if data.new_password:
            update_data["hashed_password"] = AuthService().hashed_password(
                data.new_password
            )
        try:
            await self.db.users.edit(UserUpdate(**update_data), id=user_id)
            await self.db.commit()
        except ObjectAlreadyExistsException as e:
            raise UserAlreadyExistsException from e

    async def logout_user(self, response: Response):
        """
        Удалить access_token
        """
        response.delete_cookie("access_token")

    async def delete_user(self, user_id: int):
        """
        Мягкое удаление пользователя
        """
        await self.db.users.deactivate_user(user_id)
        await self.db.commit()
