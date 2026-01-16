from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class AllocationItem(BaseModel):
    category: str
    value_kwd: int
    percentage: float
    color: Optional[str] = None


class PerformanceData(BaseModel):
    date: date
    total_value_kwd: int
    equities_value: int
    fixed_income_value: int
    real_estate_value: int
    private_funds_value: int


class AssetClassSummary(BaseModel):
    asset_class: str
    total_value_kwd: int
    cost_basis_kwd: int
    unrealized_gain_loss: int
    realized_gain_loss: int
    income_received: int
    irr_bps: Optional[int] = None
    holdings_count: int


class ExposureBreakdown(BaseModel):
    dimension: str  # geography, currency, sector, entity
    items: List[AllocationItem]


class PortfolioSummary(BaseModel):
    total_value_kwd: int
    total_cost_basis_kwd: int
    total_unrealized_gain_loss: int
    total_realized_gain_loss: int
    total_income_kwd: int
    portfolio_irr_bps: Optional[int] = None
    
    asset_class_breakdown: List[AssetClassSummary]
    allocation: List[AllocationItem]
    
    equities_count: int
    fixed_income_count: int
    properties_count: int
    units_count: int
    private_funds_count: int
    
    as_of_date: date


class IRRMatrixItem(BaseModel):
    name: str
    asset_class: str
    irr_bps: Optional[int]
    value_kwd: int


class IRRMatrix(BaseModel):
    items: List[IRRMatrixItem]
    portfolio_irr_bps: Optional[int]
