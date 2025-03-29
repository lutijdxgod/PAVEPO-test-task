from pydantic import BaseModel


class UserOut(BaseModel):
    email: str
    name: str | None
    surname: str | None
