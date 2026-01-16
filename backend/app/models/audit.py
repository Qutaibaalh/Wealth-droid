from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import BaseModel


class AuditLog(BaseModel):
    __tablename__ = "audit_logs"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT
    entity_type = Column(String(100), nullable=False)  # Table name
    entity_id = Column(UUID(as_uuid=True))
    
    old_values = Column(JSONB)
    new_values = Column(JSONB)
    
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    description = Column(Text)
