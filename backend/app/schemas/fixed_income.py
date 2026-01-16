from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID
from app.models.fixed_income import FixedIncomeType, FixedIncomeStatus


class FixedIncomeCreate(BaseModel):
    name: str
    isin: Optional[str] = None
    instrument_type: FixedIncomeType
    issuer: Optional[str] = None
    face_value_amount: int
    face_value_currency: str = "USD"
    purchase_price_amount: int
    purchase_price_currency: str
    purchase_date: date
    coupon_rate: Optional[int] = None  # Basis points
    coupon_frequency: Optional[str] = None
    maturity_date: Optional[date] = None
    expected_return_bps: Optional[int] = None
    management_fee_bps: Optional[int] = None
    is_exchange_traded: str = "no"
    notes: Optional[str] = None


class FixedIncomeUpdate(BaseModel):
    name: Optional[str] = None
    current_market_value_amount: Optional[int] = None
    current_market_value_currency: Optional[str] = None
    irr_bps: Optional[int] = None
    status: Optional[FixedIncomeStatus] = None
    notes: Optional[str] = None


class FixedIncomeResponse(BaseModel):
    id: UUID
    name: str
    isin: Optional[str]
    instrument_type: FixedIncomeType
    issuer: Optional[str]
    face_value_amount: int
    face_value_currency: str
    purchase_price_amount: int
    purchase_price_currency: str
    purchase_date: date
    coupon_rate: Optional[int]
    coupon_frequency: Optional[str]
    maturity_date: Optional[date]
    current_market_value_amount: Optional[int]
    current_market_value_currency: Optional[str]
    current_value_kwd: Optional[int]
    irr_bps: Optional[int]
    expected_return_bps: Optional[int]
    management_fee_bps: Optional[int]
    is_exchange_traded: str
    status: FixedIncomeStatus
    accrued_interest: int
    total_interest_received: int
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
