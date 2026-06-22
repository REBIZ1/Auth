from src.exceptions.exceptions import (
    ObjectNotFoundException,
    AccessRuleNotFoundHTTPException,
)
from src.schemas.access_rules import AccessRuleUpdate
from src.services.base import BaseService


class AccessRuleService(BaseService):
    async def check_rule(self, rule_id: int):
        """
        Проверить существование правила доступа
        """
        try:
            await self.db.access_rule.get_one(id=rule_id)
        except ObjectNotFoundException:
            raise AccessRuleNotFoundHTTPException

    async def get_rule(self, rule_id: int):
        return await self.db.access_rule.get_rule_by_id(rule_id)

    async def update_rule(self, rule_id: int, data: AccessRuleUpdate):
        await self.db.access_rule.edit(data, id=rule_id)
        await self.db.commit()
