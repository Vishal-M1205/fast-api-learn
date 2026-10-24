from sqlalchemy import VARCHAR, Integer, UniqueConstraint

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    __table_args__ = (UniqueConstraint("email", name="uq_user_email"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR)
    email: Mapped[str] = mapped_column(VARCHAR)
    password: Mapped[str] = mapped_column(VARCHAR)
