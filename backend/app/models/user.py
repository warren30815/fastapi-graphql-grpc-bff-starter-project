from pydantic import BaseModel
import strawberry

class UserCreate(BaseModel):
    name: str
    email: str

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True

@strawberry.type
class UserType:
    id: int
    name: str
    email: str
    is_active: bool

@strawberry.input
class UserInput:
    name: str
    email: str
