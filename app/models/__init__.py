from models.base import Base
from .advertisement import Advertisement
from .token import Token
from .user import User

ORM_OBJ = Advertisement | User | Token
ORM_CLS = type(Advertisement) | type(User) | type(Token)

__all__ = ["ORM_OBJ", "ORM_CLS", "Base", "User", "Advertisement", "Token"]
