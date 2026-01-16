from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional
from datetime import date, datetime
from uuid import UUID

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int


class MoneyAmount(BaseModel):
    amount: int  # In smallest unit (fils/cents)
    currency: str
    amount_kwd: Optional[int] = None  # Converted to KWD


class ExchangeRateResponse(BaseModel):
    from_currency: str
    to_currency: str
    rate: float
    rate_date: date
    
    class Config:
        from_attributes = True


class BaseResponse(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
