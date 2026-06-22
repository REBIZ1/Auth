from fastapi import APIRouter, Depends

from src.api.dependencies.dependencies import DBDep, CurrentUserDep, PermissionChecker
from src.schemas.access_rules import AccessRuleUpdate
from src.services.access_rules import AccessRuleService

router = APIRouter(prefix="/access_rules", tags=["Правила доступа"])


@router.get("/{rule_id}", summary="Получить правило доступа")
async def get_access_rule(
    db: DBDep,
    rule_id: int,
    current_user: CurrentUserDep,
    permission_data=Depends(PermissionChecker("access_rules")),
):
    """
    Получить правило доступа
    """
    await AccessRuleService(db).check_rule(rule_id)
    return await AccessRuleService(db).get_rule(rule_id)


@router.patch("/{rule_id}", summary="Изменить правило доступа")
async def update_access_rule(
    db: DBDep,
    rule_id: int,
    data: AccessRuleUpdate,
    current_user: CurrentUserDep,
    permission_data=Depends(PermissionChecker("access_rules")),
):
    """
    Изменить правило доступа
    """
    await AccessRuleService(db).check_rule(rule_id)
    await AccessRuleService(db).update_rule(rule_id, data)
    return {"status": "ok"}
