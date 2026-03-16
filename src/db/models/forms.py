from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class FormsModel(BaseModel):
    __tablename__ = 'forms'

    name: Mapped[str] = mapped_column(String(4), primary_key=True)
    students_count: Mapped[int] = mapped_column(Integer, nullable=False)
