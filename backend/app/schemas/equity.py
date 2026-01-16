from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID
from app.models.equity import Exchange, HoldingStatus, CorporateActionType


class EquityHoldingCreate(BaseModel):
    ticker: str
    name: str
    exchange: Exchange
    sector: Optional[str] = None
    country: Optional[str] = None
    quantity: int
    cost_basis_amount: int
    cost_basis_currency: str = "KWD"
    notes: Optional[str] = None


class EquityHoldingUpdate(BaseModel):
    name: Optional[str] = None
    sector: Optional[str] = None
    country: Optional[str] = None
    current_price_amount: Optional[int] = None
    current_price_currency: Optional[str] = None
    notes: Optional[str] = None


class EquityHoldingResponse(BaseModel):
    id: UUID
    ticker: str
    name: str
    exchange: Exchange
    sector: Optional[str]
    country: Optional[str]
    quantity: int
    cost_basis_amount: int
    cost_basis_currency: str
    current_price_amount: Optional[int]
    current_price_currency: Optional[str]
    current_value_kwd: Optional[int]
    realized_gain_loss: Optional[int] = 0
    unrealized_gain_loss: Optional[int] = 0
    status: HoldingStatus
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class EquityTransactionCreate(BaseModel):
    holding_id: UUID
    transaction_type: str  # BUY or SELL
    quantity: int
    price_amount: int
    price_currency: str
    transaction_date: date
    fees_amount: int = 0
    notes: Optional[str] = None


class EquityTransactionResponse(BaseModel):
    id: UUID
    holding_id: UUID
    transaction_type: str
    quantity: int
    price_amount: int
    price_currency: str
    total_amount: int
    total_amount_kwd: int
    transaction_date: date
    fees_amount: int
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class DividendCreate(BaseModel):
    holding_id: UUID
    amount: int
    currency: str
    ex_date: date
    payment_date: Optional[date] = None
    dividend_type: str = "cash"


class DividendResponse(BaseModel):
    id: UUID
    holding_id: UUID
    amount: int
    currency: str
    amount_kwd: int
    ex_date: date
    payment_date: Optional[date]
    dividend_type: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class CorporateActionCreate(BaseModel):
    holding_id: UUID
    action_type: CorporateActionType
    action_date: date
    ratio_from: Optional[int] = None
    ratio_to: Optional[int] = None
    shares_received: Optional[int] = None
    notes: Optional[str] = None


class CorporateActionResponse(BaseModel):
    id: UUID
    holding_id: UUID
    action_type: CorporateActionType
    action_date: date
    ratio_from: Optional[int]
    ratio_to: Optional[int]
    shares_received: Optional[int]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
