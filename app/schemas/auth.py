from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    email: str
    name: str | None
    surname: str | None
