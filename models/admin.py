from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class Admin(Document):
    firstName: str
    lastName: str
    email: EmailStr
    password: str

    class Collection:
        name = "admin"

    class Config:
        schema_extra = {
            "example": {
                "firstName": "Abdulazeez Abdulazeez Adeshina",
                "lastName": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
                "password": "3xt3m#"
            }
        }


class AdminSignIn(HTTPBasicCredentials):
    class Config:
        schema_extra = {
            "example": {
                "username": "binhkc1999@gmail.com",
                "password": "123456"
            }
        }


class AdminData(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "firstName": "Abdulazeez Abdulazeez Adeshina",
                "lastName": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
            }
        }
