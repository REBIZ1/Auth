from pydantic import BaseModel


class AccessRuleUpdate(BaseModel):
    create_permission: bool
    read_permission: bool
    read_all_permission: bool
    update_permission: bool
    update_all_permission: bool
    delete_permission: bool
    delete_all_permission: bool


class AccessRuleResponse(AccessRuleUpdate):
    id: int
    role_id: int
    element_id: int
