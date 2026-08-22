from datetime import date

from pydantic import BaseModel


class FoodSchema(BaseModel):
    form: str
    date: date
    count: int
    total: int
