from sqlalchemy import UniqueConstraint, BigInteger, String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class FoodModel(BaseModel):
    __tablename__ = 'foods'
    __table_args__ = (
        UniqueConstraint('form', 'date', name='uq_form_date'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    form: Mapped[str] = mapped_column(String, primary_key=True, autoincrement=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
