from beanie import Document
from pydantic import EmailStr

class User(Document):
    username: str
    email: EmailStr

    class Settings:
        name = "users"