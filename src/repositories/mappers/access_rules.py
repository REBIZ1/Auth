from src.models import AccessRuleOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.access_rules import AccessRuleResponse


class AccessRuleDataMapper(DataMapper):
    db_model = AccessRuleOrm
    schema = AccessRuleResponse
