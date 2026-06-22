from pydantic import EmailStr
from sqlalchemy import select, update

from src.models import UserOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.users import (
    UserDataMapper,
    UserWithHashPasswordDataMapper,
)


class UserRepository(BaseRepository):
    model = UserOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        """
        Получает пользователя по email вместе с хешированным паролем
        """
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        obj = result.scalars().one()
        return UserWithHashPasswordDataMapper.map_to_domain_entity(obj)

    async def deactivate_user(self, user_id: int):
        """
        Мягкое удаление пользователя
        """
        query = (
            update(self.model).where(self.model.id == user_id).values(is_active=False)
        )
        await self.session.execute(query)
