from datetime import datetime

from sqlalchemy import Integer, DateTime, func, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
from utils.custom_types import Role


class User(Base):
    __tablename__ = "users"
    __tableargs__ = (CheckConstraint("role in ('user', 'admin')", name="role_check"))

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(String(70), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
    tokens: Mapped[list["Token"]] = relationship(
        "Token",
        back_populates="user",
        lazy="joined",
        cascade="all, delete-orphan"
    )
    ads: Mapped[list["Advertisement"]] = relationship(
        "Advertisement",
        back_populates="user",
        lazy="joined",
        cascade="all, delete-orphan"
    )
    role: Mapped[Role] = mapped_column(String, default="user")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role
        }
