from beanie import Document, Link
from datetime import datetime
from .user import User
from .category import Category

class Transaction(Document):
    description: str
    amount: float
    type: str  
    created_at: datetime = datetime.now()

    user: Link[User]
    category: Link[Category]

    class Settings:
        name = "transactions"