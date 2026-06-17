from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.access_rules import AccessRuleOrm


class BusinessElementOrm(Base):
    __tablename__ = "business_elements"

    __table_args__ = (
        CheckConstraint("length(name) >= 1", name="business_element_name_check"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)

    access_rules: Mapped[list["AccessRuleOrm"]] = relationship(
        "AccessRuleOrm", back_populates="element", cascade="all, delete-orphan"
    )
