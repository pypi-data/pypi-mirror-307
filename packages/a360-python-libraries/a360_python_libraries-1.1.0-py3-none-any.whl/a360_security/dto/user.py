import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    username: str
    email: Optional[EmailStr]
    sub: uuid.UUID
    roles: list[str]
    practice_id: Optional[uuid.UUID]
    is_admin: bool
    is_practice_dependant: bool
    is_active: bool

    class Config:
        from_attributes = True
