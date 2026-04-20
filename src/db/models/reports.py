from sqlalchemy import String, BigInteger, Date, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel

class ReportModel(BaseModel):
    __tablename__ = "reports"
    __table_args__ = (
        UniqueConstraint("form", "date", name="uq_form_date"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    form: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    absentees: Mapped[int] = mapped_column(Integer, nullable=False)
    patients: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
