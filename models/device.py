from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel, EmailStr


class Device(Document):
    id: str
    device_name: str
    manufacture: str
    mac_address: str
    link_image: str
    status: int

    class Config:
        schema_extra = {
            "example": {
                "id": "123",
                "device_name": "Amazon Echo Dot 4",
                "manufacture": "smarthomekit",
                "mac_address": "12:34:56:78:fg:wf",
                "link_image": "/home/hoangtrongbinh/temp.png",
                "status": 1
            }
        }


class UpdateDeviceModel(BaseModel):
    device_name: Optional[str]
    manufacture: Optional[str]
    mac_address: Optional[str]
    link_image: Optional[str]
    status: Optional[int]

    class Collection:
        name = "device"

    class Config:
        schema_extra = {
            "example": {
                "device_name": "Amazon Echo Dot 4",
                "manufacture": "smarthomekit",
                "mac_address": "12:34:56:78:fg:wf",
                "link_image": "/home/hoangtrongbinh/temp.png",
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
