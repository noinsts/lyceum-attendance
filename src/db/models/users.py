from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    form: Mapped[str] = mapped_column(String(4), nullable=False)
