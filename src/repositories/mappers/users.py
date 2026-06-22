from src.models import UserOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.users import User, UserWithHashPassword


class UserDataMapper(DataMapper):
    db_model = UserOrm
    schema = User


class UserWithHashPasswordDataMapper(DataMapper):
    db_model = UserOrm
    schema = UserWithHashPassword
