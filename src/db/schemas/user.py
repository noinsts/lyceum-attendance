from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: int
    name: str
    form: str
