from typing import Optional, Any, Union

from pydantic import BaseModel


class ServiceResponse(BaseModel):
    code: int
    data: Optional[dict] = None

    class Config:
        from_attributes = True
