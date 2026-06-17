from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, CheckConstraint

from src.core.database import Base
from src.models.users import UserOrm

if TYPE_CHECKING:
    from src.models.access_rules import AccessRuleOrm


class RoleOrm(Base):
    __tablename__ = "roles"

    __table_args__ = (CheckConstraint("length(name) >= 1", name="name_check"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)

    users: Mapped[list["UserOrm"]] = relationship("UserOrm", back_populates="role")
    access_rules: Mapped[list["AccessRuleOrm"]] = relationship(
        "AccessRuleOrm", back_populates="role", cascade="all, delete-orphan"
    )
