from src.repositories.users import UserRepository
from src.repositories.access_rules import AccessRuleRepository


class DBManager:
    """
    Менеджер работы с базой данных
    создает сессии и предоставляет доступ к репозиториям
    """

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.access_rule = AccessRuleRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
