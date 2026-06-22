from src.exceptions.exceptions import ForbiddenHTTPException, ForbiddenException
from src.schemas.users import User
from src.core.db_manager import DBManager


class BaseService:
    def __init__(self, db: DBManager | None = None) -> None:
        self.db = db

    async def check_owner_permission(
        self, element: str, permission: str, user_id: int, current_user: User
    ):
        """
        Проверка доступа к чужим данным
        """
        permission_all_map = {
            "read_permission": "read_all_permission",
            "update_permission": "update_all_permission",
            "delete_permission": "delete_all_permission",
        }
        rule = await self.db.access_rule.get_rule(
            role_id=current_user.role_id,
            element_name=element,
        )
        if current_user.id == user_id:
            allowed = getattr(rule, permission)
        else:
            permission_all = permission_all_map[permission]
            allowed = getattr(rule, permission_all)
        if not allowed:
            raise ForbiddenException
