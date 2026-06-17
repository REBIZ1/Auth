from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.roles import RoleOrm
    from src.models.business_elements import BusinessElementOrm


class AccessRuleOrm(Base):
    __tablename__ = "access_rules"

    __table_args__ = (
        UniqueConstraint("role_id", "element_id", name="unique_role_element_rule"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    element_id: Mapped[int] = mapped_column(
        ForeignKey("business_elements.id", ondelete="CASCADE"), nullable=False
    )
    create_permission: Mapped[bool] = mapped_column(
        nullable=False, server_default=text("false")
    )
    read_permission: Mapped[bool] = mapped_column(
        nullable=False, server_default=text("false")
    )
    read_all_permission: Mapped[bool] = mapped_column(
        nullable=False, server_default=text("false")
    )
    update_permission: Mapped[bool] = mapped_column(
        nullable=False, server_default=text("false")
    )
    update_all_permission: Mapped[bool] = mapped_column(
        nullable=False, server_default=text("false")
    )
    delete_permission: Mapped[bool] = mapped_column(
        nullable=False, server_default=text("false")
    )
    delete_all_permission: Mapped[bool] = mapped_column(
        nullable=False, server_default=text("false")
    )

    role: Mapped["RoleOrm"] = relationship("RoleOrm", back_populates="access_rules")
    element: Mapped["BusinessElementOrm"] = relationship(
        "BusinessElementOrm", back_populates="access_rules"
    )
