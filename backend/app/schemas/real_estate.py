from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID
from app.models.real_estate import PropertyType, UnitStatus


class PropertyCreate(BaseModel):
    name: str
    property_type: PropertyType
    address: Optional[str] = None
    city: Optional[str] = None
    country: str = "Kuwait"
    purchase_price_amount: int
    purchase_price_currency: str = "KWD"
    purchase_date: date
    ownership_entity: Optional[str] = None
    ownership_percentage: int = 10000  # 100%
    total_area_sqm: Optional[int] = None
    notes: Optional[str] = None


class PropertyUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    current_value_amount: Optional[int] = None
    current_value_currency: Optional[str] = None
    ownership_entity: Optional[str] = None
    irr_bps: Optional[int] = None
    notes: Optional[str] = None


class UnitCreate(BaseModel):
    property_id: UUID
    unit_number: str
    unit_type: Optional[str] = None
    floor: Optional[int] = None
    area_sqm: Optional[int] = None
    monthly_rent_amount: Optional[int] = None
    monthly_rent_currency: str = "KWD"
    budgeted_rent_amount: Optional[int] = None
    notes: Optional[str] = None


class UnitUpdate(BaseModel):
    unit_type: Optional[str] = None
    status: Optional[UnitStatus] = None
    tenant_name: Optional[str] = None
    lease_start_date: Optional[date] = None
    lease_end_date: Optional[date] = None
    monthly_rent_amount: Optional[int] = None
    budgeted_rent_amount: Optional[int] = None
    outstanding_amount: Optional[int] = None
    notes: Optional[str] = None


class UnitResponse(BaseModel):
    id: UUID
    property_id: UUID
    unit_number: str
    unit_type: Optional[str]
    floor: Optional[int]
    area_sqm: Optional[int]
    status: UnitStatus
    tenant_name: Optional[str]
    lease_start_date: Optional[date]
    lease_end_date: Optional[date]
    monthly_rent_amount: Optional[int]
    monthly_rent_currency: str
    budgeted_rent_amount: Optional[int]
    deposit_amount: int
    outstanding_amount: int
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class PropertyResponse(BaseModel):
    id: UUID
    name: str
    property_type: PropertyType
    address: Optional[str]
    city: Optional[str]
    country: str
    purchase_price_amount: int
    purchase_price_currency: str
    purchase_date: date
    current_value_amount: Optional[int]
    current_value_currency: Optional[str]
    last_valuation_date: Optional[date]
    ownership_entity: Optional[str]
    ownership_percentage: int
    total_area_sqm: Optional[int]
    irr_bps: Optional[int]
    notes: Optional[str]
    units: List[UnitResponse] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RentalIncomeCreate(BaseModel):
    unit_id: UUID
    period_start: date
    period_end: date
    expected_amount: int
    received_amount: int = 0
    currency: str = "KWD"
    payment_date: Optional[date] = None
    is_collected: bool = False
    notes: Optional[str] = None


class RentalIncomeResponse(BaseModel):
    id: UUID
    unit_id: UUID
    period_start: date
    period_end: date
    expected_amount: int
    received_amount: int
    currency: str
    payment_date: Optional[date]
    is_collected: bool
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class PropertyExpenseCreate(BaseModel):
    property_id: UUID
    unit_id: Optional[UUID] = None
    expense_type: str
    description: Optional[str] = None
    amount: int
    currency: str = "KWD"
    expense_date: date
    vendor_name: Optional[str] = None
    invoice_number: Optional[str] = None


class PropertyExpenseResponse(BaseModel):
    id: UUID
    property_id: UUID
    unit_id: Optional[UUID]
    expense_type: str
    description: Optional[str]
    amount: int
    currency: str
    expense_date: date
    vendor_name: Optional[str]
    invoice_number: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class OccupancyReport(BaseModel):
    property_id: UUID
    property_name: str
    total_units: int
    occupied_units: int
    vacant_units: int
    occupancy_rate: float
    total_monthly_rent: int
    total_collected: int
    total_outstanding: int
    currency: str = "KWD"
