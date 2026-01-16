from sqlalchemy import Column, String, BigInteger, Date, ForeignKey, Enum, Text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class FundType(str, enum.Enum):
    PRIVATE_EQUITY = "private_equity"
    VENTURE_CAPITAL = "venture_capital"
    HEDGE_FUND = "hedge_fund"
    REAL_ESTATE_FUND = "real_estate_fund"
    INFRASTRUCTURE = "infrastructure"
    DIRECT_INVESTMENT = "direct_investment"
    CO_INVESTMENT = "co_investment"


class FundStatus(str, enum.Enum):
    ACTIVE = "active"
    FULLY_REALIZED = "fully_realized"
    PARTIALLY_REALIZED = "partially_realized"
    WRITTEN_OFF = "written_off"


class PrivateFund(BaseModel):
    __tablename__ = "private_funds"
    
    name = Column(String(255), nullable=False)
    fund_type = Column(Enum(FundType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    fund_manager = Column(String(255))
    
    vintage_year = Column(Integer)
    geography = Column(String(100))
    sector = Column(String(100))
    
    committed_capital_amount = Column(BigInteger, nullable=False)
    committed_capital_currency = Column(String(3), default="USD")
    
    called_capital_amount = Column(BigInteger, default=0)
    uncalled_capital_amount = Column(BigInteger)
    
    distributions_declared = Column(BigInteger, default=0)
    distributions_received = Column(BigInteger, default=0)
    
    current_nav_amount = Column(BigInteger)
    current_nav_currency = Column(String(3), default="USD")
    current_nav_kwd = Column(BigInteger)
    nav_date = Column(Date)
    
    irr_bps = Column(Integer)  # IRR in basis points
    tvpi_bps = Column(Integer)  # TVPI in basis points (e.g., 15000 = 1.5x)
    dpi_bps = Column(Integer)  # DPI in basis points
    
    management_fee_bps = Column(Integer)  # Annual management fee
    carried_interest_bps = Column(Integer)  # Carry percentage
    
    fund_term_years = Column(Integer)
    investment_period_end = Column(Date)
    fund_end_date = Column(Date)
    
    status = Column(Enum(FundStatus, values_callable=lambda x: [e.value for e in x]), default=FundStatus.ACTIVE)
    notes = Column(Text)
    
    capital_calls = relationship("CapitalCall", back_populates="fund")
    distributions = relationship("Distribution", back_populates="fund")
    valuations = relationship("FundValuation", back_populates="fund")


class CapitalCall(BaseModel):
    __tablename__ = "capital_calls"
    
    fund_id = Column(UUID(as_uuid=True), ForeignKey("private_funds.id"), nullable=False)
    call_number = Column(Integer)
    
    call_date = Column(Date, nullable=False)
    due_date = Column(Date)
    payment_date = Column(Date)
    
    amount = Column(BigInteger, nullable=False)
    currency = Column(String(3), default="USD")
    amount_kwd = Column(BigInteger)
    
    purpose = Column(String(255))  # investment, fees, expenses
    is_paid = Column(Boolean, default=False)
    
    notes = Column(Text)
    
    fund = relationship("PrivateFund", back_populates="capital_calls")


class Distribution(BaseModel):
    __tablename__ = "distributions"
    
    fund_id = Column(UUID(as_uuid=True), ForeignKey("private_funds.id"), nullable=False)
    distribution_number = Column(Integer)
    
    declaration_date = Column(Date, nullable=False)
    payment_date = Column(Date)
    
    amount = Column(BigInteger, nullable=False)
    currency = Column(String(3), default="USD")
    amount_kwd = Column(BigInteger)
    
    distribution_type = Column(String(50))  # return_of_capital, profit, dividend
    is_received = Column(Boolean, default=False)
    
    notes = Column(Text)
    
    fund = relationship("PrivateFund", back_populates="distributions")


class FundValuation(BaseModel):
    __tablename__ = "fund_valuations"
    
    fund_id = Column(UUID(as_uuid=True), ForeignKey("private_funds.id"), nullable=False)
    valuation_date = Column(Date, nullable=False)
    
    nav_amount = Column(BigInteger, nullable=False)
    currency = Column(String(3), default="USD")
    nav_kwd = Column(BigInteger)
    
    irr_bps = Column(Integer)
    tvpi_bps = Column(Integer)
    
    notes = Column(Text)
    
    fund = relationship("PrivateFund", back_populates="valuations")
