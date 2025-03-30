from datetime import datetime
from pydantic import BaseModel


class FileOut(BaseModel):
    id: int
    filename: str
    filepath: str
    uploaded_at: datetime
