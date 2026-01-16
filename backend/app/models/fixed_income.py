from sqlalchemy import Column, String, BigInteger, Date, Enum, Text, Integer
import enum
from app.models.base import BaseModel


class FixedIncomeType(str, enum.Enum):
    CORPORATE_BOND = "corporate_bond"
    GOVERNMENT_BOND = "government_bond"
    SUKUK = "sukuk"
    FIXED_INCOME_FUND = "fixed_income_fund"
    TREASURY = "treasury"


class FixedIncomeStatus(str, enum.Enum):
    ACTIVE = "active"
    MATURED = "matured"
    SOLD = "sold"
    DEFAULTED = "defaulted"


class FixedIncomeHolding(BaseModel):
    __tablename__ = "fixed_income_holdings"
    
    name = Column(String(255), nullable=False)
    isin = Column(String(20), index=True)
    instrument_type = Column(Enum(FixedIncomeType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    issuer = Column(String(255))
    
    face_value_amount = Column(BigInteger, nullable=False)  # In smallest unit
    face_value_currency = Column(String(3), nullable=False, default="USD")
    
    purchase_price_amount = Column(BigInteger, nullable=False)  # Cost basis
    purchase_price_currency = Column(String(3), nullable=False)
    purchase_date = Column(Date, nullable=False)
    
    coupon_rate = Column(Integer)  # Basis points (e.g., 500 = 5.00%)
    coupon_frequency = Column(String(20))  # annual, semi-annual, quarterly
    maturity_date = Column(Date)
    
    current_market_value_amount = Column(BigInteger)
    current_market_value_currency = Column(String(3))
    current_value_kwd = Column(BigInteger)
    
    irr_bps = Column(Integer)  # IRR in basis points
    expected_return_bps = Column(Integer)  # Promised return in basis points
    management_fee_bps = Column(Integer)  # For funds
    
    is_exchange_traded = Column(String(10), default="no")
    status = Column(Enum(FixedIncomeStatus, values_callable=lambda x: [e.value for e in x]), default=FixedIncomeStatus.ACTIVE)
    
    accrued_interest = Column(BigInteger, default=0)
    total_interest_received = Column(BigInteger, default=0)
    
    notes = Column(Text)
