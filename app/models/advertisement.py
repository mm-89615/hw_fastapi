
from datetime import datetime

from sqlalchemy import Integer, DECIMAL, DateTime, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class Advertisement(Base):
    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=False)
    user: Mapped["User"] = relationship("User", back_populates="ads", lazy="joined")

    @property
    def dict(self): return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "price": self.price,
        "user_id": self.user_id,
        "created_at": self.created_at.isoformat(),
        "updated_at": self.updated_at.isoformat(),
    }
