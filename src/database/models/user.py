from __future__ import annotations

from typing import Optional

from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class DBUser(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True, primary_key=True) # telegram_id
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"<User {self.username or self.id}>"

    def get_tg_link(self):
        if self.username is not None:
            return f'https://t.me/{self.username}'
        else:
            return f'https://t.me/@id{self.id}'
