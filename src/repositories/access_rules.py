from sqlalchemy import select

from src.repositories.mappers.access_rules import AccessRuleDataMapper
from src.models import AccessRuleOrm, BusinessElementOrm
from src.repositories.base import BaseRepository


class AccessRuleRepository(BaseRepository):
    model = AccessRuleOrm
    mapper = AccessRuleDataMapper

    async def get_rule(self, role_id: int, element_name: str):
        """
        Получает правило доступа для указанной роли и бизнес элемента
        """
        query = (
            select(self.model)
            .join(BusinessElementOrm, self.model.element_id == BusinessElementOrm.id)
            .where(
                self.model.role_id == role_id,
                BusinessElementOrm.name == element_name,
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def get_rule_by_id(self, rule_id: int):
        """
        Получает правило доступа по его идентификатору
        """
        query = select(self.model).where(self.model.id == rule_id)
        result = await self.session.execute(query)
        obj = result.scalars().one()
        return AccessRuleDataMapper.map_to_domain_entity(obj)
