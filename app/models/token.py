import uuid
from datetime import datetime

from sqlalchemy import Integer, DateTime, func, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(
        UUID,
        unique=True,
        server_default=func.gen_random_uuid()
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=False)
    user: Mapped["User"] = relationship("User", back_populates="tokens", lazy="joined")

    @property
    def dict(self):
        return {"token": self.token}
