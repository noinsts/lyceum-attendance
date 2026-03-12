from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class AdminModel(BaseModel):
    __tablename__ = 'admins'
    
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
