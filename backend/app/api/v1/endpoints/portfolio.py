from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.equity import EquityHolding
from app.models.fixed_income import FixedIncomeHolding
from app.models.real_estate import Property, Unit
from app.models.private_fund import PrivateFund
from app.schemas.portfolio import PortfolioSummary, AllocationItem, AssetClassSummary, ExposureBreakdown
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/summary", response_model=PortfolioSummary)
def get_portfolio_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Equities
    equities = db.query(EquityHolding).filter(EquityHolding.deleted_at.is_(None)).all()
    equities_value = sum(e.current_value_kwd or 0 for e in equities)
    equities_cost = sum(e.cost_basis_amount or 0 for e in equities)
    equities_unrealized = sum(e.unrealized_gain_loss or 0 for e in equities)
    equities_realized = sum(e.realized_gain_loss or 0 for e in equities)
    
    # Fixed Income
    fixed_income = db.query(FixedIncomeHolding).filter(FixedIncomeHolding.deleted_at.is_(None)).all()
    fi_value = sum(f.current_value_kwd or f.purchase_price_amount or 0 for f in fixed_income)
    fi_cost = sum(f.purchase_price_amount or 0 for f in fixed_income)
    fi_income = sum(f.total_interest_received or 0 for f in fixed_income)
    
    # Real Estate
    properties = db.query(Property).filter(Property.deleted_at.is_(None)).all()
    re_value = sum(p.current_value_amount or p.purchase_price_amount or 0 for p in properties)
    re_cost = sum(p.purchase_price_amount or 0 for p in properties)
    
    units_count = db.query(Unit).filter(Unit.deleted_at.is_(None)).count()
    
    # Private Funds
    funds = db.query(PrivateFund).filter(PrivateFund.deleted_at.is_(None)).all()
    pf_value = sum(f.current_nav_kwd or f.called_capital_amount or 0 for f in funds)
    pf_cost = sum(f.called_capital_amount or 0 for f in funds)
    pf_distributions = sum(f.distributions_received or 0 for f in funds)
    
    # Totals
    total_value = equities_value + fi_value + re_value + pf_value
    total_cost = equities_cost + fi_cost + re_cost + pf_cost
    total_unrealized = equities_unrealized + (fi_value - fi_cost) + (re_value - re_cost) + (pf_value - pf_cost)
    total_income = fi_income + pf_distributions
    
    # Allocation
    allocation = []
    if total_value > 0:
        if equities_value > 0:
            allocation.append(AllocationItem(
                category="Public Equities",
                value_kwd=equities_value,
                percentage=round(equities_value / total_value * 100, 2),
                color="#3B82F6"
            ))
        if fi_value > 0:
            allocation.append(AllocationItem(
                category="Fixed Income",
                value_kwd=fi_value,
                percentage=round(fi_value / total_value * 100, 2),
                color="#10B981"
            ))
        if re_value > 0:
            allocation.append(AllocationItem(
                category="Real Estate",
                value_kwd=re_value,
                percentage=round(re_value / total_value * 100, 2),
                color="#F59E0B"
            ))
        if pf_value > 0:
            allocation.append(AllocationItem(
                category="Private Funds",
                value_kwd=pf_value,
                percentage=round(pf_value / total_value * 100, 2),
                color="#8B5CF6"
            ))
    
    # Asset class summaries
    asset_class_breakdown = [
        AssetClassSummary(
            asset_class="Public Equities",
            total_value_kwd=equities_value,
            cost_basis_kwd=equities_cost,
            unrealized_gain_loss=equities_unrealized,
            realized_gain_loss=equities_realized,
            income_received=0,
            holdings_count=len(equities)
        ),
        AssetClassSummary(
            asset_class="Fixed Income",
            total_value_kwd=fi_value,
            cost_basis_kwd=fi_cost,
            unrealized_gain_loss=fi_value - fi_cost,
            realized_gain_loss=0,
            income_received=fi_income,
            holdings_count=len(fixed_income)
        ),
        AssetClassSummary(
            asset_class="Real Estate",
            total_value_kwd=re_value,
            cost_basis_kwd=re_cost,
            unrealized_gain_loss=re_value - re_cost,
            realized_gain_loss=0,
            income_received=0,
            holdings_count=len(properties)
        ),
        AssetClassSummary(
            asset_class="Private Funds",
            total_value_kwd=pf_value,
            cost_basis_kwd=pf_cost,
            unrealized_gain_loss=pf_value - pf_cost,
            realized_gain_loss=0,
            income_received=pf_distributions,
            holdings_count=len(funds)
        ),
    ]
    
    return PortfolioSummary(
        total_value_kwd=total_value,
        total_cost_basis_kwd=total_cost,
        total_unrealized_gain_loss=total_unrealized,
        total_realized_gain_loss=equities_realized,
        total_income_kwd=total_income,
        asset_class_breakdown=asset_class_breakdown,
        allocation=allocation,
        equities_count=len(equities),
        fixed_income_count=len(fixed_income),
        properties_count=len(properties),
        units_count=units_count,
        private_funds_count=len(funds),
        as_of_date=date.today()
    )


@router.get("/exposure/geography", response_model=ExposureBreakdown)
def get_geography_exposure(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Aggregate by geography
    exposure = {}
    
    # Equities
    equities = db.query(EquityHolding).filter(EquityHolding.deleted_at.is_(None)).all()
    for e in equities:
        country = e.country or "Unknown"
        exposure[country] = exposure.get(country, 0) + (e.current_value_kwd or 0)
    
    # Real Estate
    properties = db.query(Property).filter(Property.deleted_at.is_(None)).all()
    for p in properties:
        country = p.country or "Unknown"
        exposure[country] = exposure.get(country, 0) + (p.current_value_amount or p.purchase_price_amount or 0)
    
    # Private Funds
    funds = db.query(PrivateFund).filter(PrivateFund.deleted_at.is_(None)).all()
    for f in funds:
        geo = f.geography or "Global"
        exposure[geo] = exposure.get(geo, 0) + (f.current_nav_kwd or f.called_capital_amount or 0)
    
    total = sum(exposure.values())
    items = [
        AllocationItem(
            category=k,
            value_kwd=v,
            percentage=round(v / total * 100, 2) if total > 0 else 0
        )
        for k, v in sorted(exposure.items(), key=lambda x: -x[1])
    ]
    
    return ExposureBreakdown(dimension="geography", items=items)


@router.get("/exposure/currency", response_model=ExposureBreakdown)
def get_currency_exposure(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    exposure = {}
    
    equities = db.query(EquityHolding).filter(EquityHolding.deleted_at.is_(None)).all()
    for e in equities:
        curr = e.current_price_currency or e.cost_basis_currency or "KWD"
        exposure[curr] = exposure.get(curr, 0) + (e.current_value_kwd or 0)
    
    fixed_income = db.query(FixedIncomeHolding).filter(FixedIncomeHolding.deleted_at.is_(None)).all()
    for f in fixed_income:
        curr = f.face_value_currency or "USD"
        exposure[curr] = exposure.get(curr, 0) + (f.current_value_kwd or f.purchase_price_amount or 0)
    
    funds = db.query(PrivateFund).filter(PrivateFund.deleted_at.is_(None)).all()
    for f in funds:
        curr = f.committed_capital_currency or "USD"
        exposure[curr] = exposure.get(curr, 0) + (f.current_nav_kwd or f.called_capital_amount or 0)
    
    total = sum(exposure.values())
    items = [
        AllocationItem(
            category=k,
            value_kwd=v,
            percentage=round(v / total * 100, 2) if total > 0 else 0
        )
        for k, v in sorted(exposure.items(), key=lambda x: -x[1])
    ]
    
    return ExposureBreakdown(dimension="currency", items=items)


@router.get("/exposure/sector", response_model=ExposureBreakdown)
def get_sector_exposure(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    exposure = {}
    
    equities = db.query(EquityHolding).filter(EquityHolding.deleted_at.is_(None)).all()
    for e in equities:
        sector = e.sector or "Other"
        exposure[sector] = exposure.get(sector, 0) + (e.current_value_kwd or 0)
    
    funds = db.query(PrivateFund).filter(PrivateFund.deleted_at.is_(None)).all()
    for f in funds:
        sector = f.sector or "Diversified"
        exposure[sector] = exposure.get(sector, 0) + (f.current_nav_kwd or f.called_capital_amount or 0)
    
    total = sum(exposure.values())
    items = [
        AllocationItem(
            category=k,
            value_kwd=v,
            percentage=round(v / total * 100, 2) if total > 0 else 0
        )
        for k, v in sorted(exposure.items(), key=lambda x: -x[1])
    ]
    
    return ExposureBreakdown(dimension="sector", items=items)
