from pydantic import BaseModel
import enum
from fastapi import Query


class Role(str, enum.Enum):
    admin: str = "admin"
    personel: str = "personel"

class User(BaseModel):
    name: str
    password: str
    # check if email is valid, ... means the parameter is required. can also be set to None
    email: str = Query(..., regex="^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
    role: Role
