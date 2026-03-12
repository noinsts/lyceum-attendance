from datetime import date

from pydantic import BaseModel


class ReportSchema(BaseModel):
    form: str
    date: date
    absentees: int
    patients: int
