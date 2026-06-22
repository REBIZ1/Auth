from sqlalchemy import select

from src.models import AccessRuleOrm, BusinessElementOrm
from src.repositories.base import BaseRepository


class AccessRuleRepository(BaseRepository):
    model = AccessRuleOrm

    async def get_rule(self, role_id: int, element_name: str):
        """
        Метод получения правила
        """
        query = (
            select(AccessRuleOrm)
            .join(BusinessElementOrm, AccessRuleOrm.element_id == BusinessElementOrm.id)
            .where(
                AccessRuleOrm.role_id == role_id,
                BusinessElementOrm.name == element_name,
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one()
