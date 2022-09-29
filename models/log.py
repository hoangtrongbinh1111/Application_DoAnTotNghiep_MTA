from datetime import datetime
from typing import Optional, Any
import time
from beanie import Document
from pydantic import BaseModel, EmailStr


class Log(Document):
    id: str
    label_detect: str
    mac_address: str
    time_detect: datetime
    status: int

    class Config:
        schema_extra = {
            "example": {
                "id": "123",
                "label_detect": "Amazon Echo Dot 4",
                "mac_address": "12:34:56:78:fg:wf",
                "time_detect": time.time(),
                "status": 1
            }
        }

class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data"
            }
        }
