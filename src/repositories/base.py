import logging

from pydantic import BaseModel
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import insert, update, select
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.exceptions.exceptions import (
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
)
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper

    def __init__(self, session):
        self.session = session

    async def add(self, data: BaseModel):
        """
        Добавляет данные в БД
        """
        try:
            add_stmt = (
                insert(self.model).values(**data.model_dump()).returning(self.model)
            )
            result = await self.session.execute(add_stmt)
            obj = result.scalars().one()
            return self.mapper.map_to_domain_entity(obj)
        except IntegrityError as e:
            logging.error(
                f"Не удалось добавить данные в БД, тип ошибки: {type(e.orig.__cause__)=}"
            )
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from e
            else:
                logging.error(
                    f"Незнакомая ошибка, тип ошибки: {type(e.orig.__cause__)=}"
                )
                raise e

    async def edit(self, data: BaseModel, exclude_unset: bool = True, **filter_by):
        """
        Изменяет данные в БД, если exclude_unset = True, то изменяет частично
        """
        try:
            edit_stmt = (
                update(self.model)
                .filter_by(**filter_by)
                .values(**data.model_dump(exclude_unset=exclude_unset))
            )
            await self.session.execute(edit_stmt)
        except IntegrityError as e:
            logging.error(
                f"Не удалось добавить данные в БД, тип ошибки: {type(e.orig.__cause__)=}"
            )
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from e
            else:
                logging.error(
                    f"Незнакомая ошибка, тип ошибки: {type(e.orig.__cause__)=}"
                )
                raise e

    async def get_one(self, **filter_by) -> BaseModel:
        """
        Принимает аргументы для фильтрации и возвращает одно значение,
        в случае отсутсвия значения возвращает ошибку ObjectNotFoundException
        """
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            obj = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(obj)
