from pydantic import BaseModel


class UserUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
