from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID
from app.models.private_fund import FundType, FundStatus


class PrivateFundCreate(BaseModel):
    name: str
    fund_type: FundType
    fund_manager: Optional[str] = None
    vintage_year: Optional[int] = None
    geography: Optional[str] = None
    sector: Optional[str] = None
    committed_capital_amount: int
    committed_capital_currency: str = "USD"
    management_fee_bps: Optional[int] = None
    carried_interest_bps: Optional[int] = None
    fund_term_years: Optional[int] = None
    investment_period_end: Optional[date] = None
    fund_end_date: Optional[date] = None
    notes: Optional[str] = None


class PrivateFundUpdate(BaseModel):
    name: Optional[str] = None
    fund_manager: Optional[str] = None
    current_nav_amount: Optional[int] = None
    current_nav_currency: Optional[str] = None
    nav_date: Optional[date] = None
    irr_bps: Optional[int] = None
    tvpi_bps: Optional[int] = None
    dpi_bps: Optional[int] = None
    status: Optional[FundStatus] = None
    notes: Optional[str] = None


class PrivateFundResponse(BaseModel):
    id: UUID
    name: str
    fund_type: FundType
    fund_manager: Optional[str]
    vintage_year: Optional[int]
    geography: Optional[str]
    sector: Optional[str]
    committed_capital_amount: int
    committed_capital_currency: str
    called_capital_amount: int
    uncalled_capital_amount: Optional[int]
    distributions_declared: int
    distributions_received: int
    current_nav_amount: Optional[int]
    current_nav_currency: Optional[str]
    current_nav_kwd: Optional[int]
    nav_date: Optional[date]
    irr_bps: Optional[int]
    tvpi_bps: Optional[int]
    dpi_bps: Optional[int]
    management_fee_bps: Optional[int]
    carried_interest_bps: Optional[int]
    fund_term_years: Optional[int]
    investment_period_end: Optional[date]
    fund_end_date: Optional[date]
    status: FundStatus
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CapitalCallCreate(BaseModel):
    fund_id: UUID
    call_number: Optional[int] = None
    call_date: date
    due_date: Optional[date] = None
    amount: int
    currency: str = "USD"
    purpose: Optional[str] = None
    notes: Optional[str] = None


class CapitalCallResponse(BaseModel):
    id: UUID
    fund_id: UUID
    call_number: Optional[int]
    call_date: date
    due_date: Optional[date]
    payment_date: Optional[date]
    amount: int
    currency: str
    amount_kwd: Optional[int]
    purpose: Optional[str]
    is_paid: bool
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class DistributionCreate(BaseModel):
    fund_id: UUID
    distribution_number: Optional[int] = None
    declaration_date: date
    payment_date: Optional[date] = None
    amount: int
    currency: str = "USD"
    distribution_type: Optional[str] = None
    notes: Optional[str] = None


class DistributionResponse(BaseModel):
    id: UUID
    fund_id: UUID
    distribution_number: Optional[int]
    declaration_date: date
    payment_date: Optional[date]
    amount: int
    currency: str
    amount_kwd: Optional[int]
    distribution_type: Optional[str]
    is_received: bool
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
