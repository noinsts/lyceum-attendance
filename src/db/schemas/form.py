from pydantic import BaseModel


class FormSchema(BaseModel):
    name: str
    students_count: int
