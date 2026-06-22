from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey, CheckConstraint, text

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.roles import RoleOrm


class UserOrm(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint("length(first_name) >= 1", name="first_name_check"),
        CheckConstraint("length(last_name) >= 1", name="last_name_check"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150))
    middle_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), nullable=False, server_default=text("1")
    )

    role: Mapped["RoleOrm"] = relationship("RoleOrm", back_populates="users")
