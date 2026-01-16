from sqlalchemy import Column, String, Boolean, Enum
import enum
from app.models.base import BaseModel


class UserRole(str, enum.Enum):
    admin = "admin"
    cfo = "cfo"
    ic_member = "ic_member"
    accountant = "accountant"
    viewer = "viewer"


class User(BaseModel):
    __tablename__ = "users"
    
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, values_callable=lambda x: [e.value for e in x]), default=UserRole.viewer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
