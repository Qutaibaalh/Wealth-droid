from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.core.database import get_db
from app.models.user import User
from app.models.private_fund import PrivateFund, CapitalCall, Distribution, FundValuation, FundType
from app.schemas.private_fund import (
    PrivateFundCreate, PrivateFundUpdate, PrivateFundResponse,
    CapitalCallCreate, CapitalCallResponse,
    DistributionCreate, DistributionResponse
)
from app.schemas.common import PaginatedResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("", response_model=PaginatedResponse[PrivateFundResponse])
def list_private_funds(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    fund_type: Optional[FundType] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(PrivateFund).filter(PrivateFund.deleted_at.is_(None))
    
    if fund_type:
        query = query.filter(PrivateFund.fund_type == fund_type)
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.post("", response_model=PrivateFundResponse, status_code=status.HTTP_201_CREATED)
def create_private_fund(
    fund_in: PrivateFundCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fund = PrivateFund(**fund_in.model_dump())
    fund.uncalled_capital_amount = fund.committed_capital_amount
    db.add(fund)
    db.commit()
    db.refresh(fund)
    return fund


@router.get("/{fund_id}", response_model=PrivateFundResponse)
def get_private_fund(
    fund_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fund = db.query(PrivateFund).filter(
        PrivateFund.id == fund_id,
        PrivateFund.deleted_at.is_(None)
    ).first()
    
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    return fund


@router.put("/{fund_id}", response_model=PrivateFundResponse)
def update_private_fund(
    fund_id: UUID,
    fund_in: PrivateFundUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fund = db.query(PrivateFund).filter(
        PrivateFund.id == fund_id,
        PrivateFund.deleted_at.is_(None)
    ).first()
    
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    
    for field, value in fund_in.model_dump(exclude_unset=True).items():
        setattr(fund, field, value)
    
    db.commit()
    db.refresh(fund)
    return fund


@router.delete("/{fund_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_private_fund(
    fund_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fund = db.query(PrivateFund).filter(
        PrivateFund.id == fund_id,
        PrivateFund.deleted_at.is_(None)
    ).first()
    
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    
    fund.deleted_at = datetime.utcnow()
    db.commit()


# Capital Calls
@router.get("/{fund_id}/capital-calls", response_model=List[CapitalCallResponse])
def list_capital_calls(
    fund_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    calls = db.query(CapitalCall).filter(
        CapitalCall.fund_id == fund_id,
        CapitalCall.deleted_at.is_(None)
    ).order_by(CapitalCall.call_date.desc()).all()
    return calls


@router.post("/{fund_id}/capital-calls", response_model=CapitalCallResponse, status_code=status.HTTP_201_CREATED)
def create_capital_call(
    fund_id: UUID,
    call_in: CapitalCallCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fund = db.query(PrivateFund).filter(
        PrivateFund.id == fund_id,
        PrivateFund.deleted_at.is_(None)
    ).first()
    
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    
    call = CapitalCall(fund_id=fund_id, **call_in.model_dump(exclude={"fund_id"}))
    db.add(call)
    db.commit()
    db.refresh(call)
    return call


@router.put("/{fund_id}/capital-calls/{call_id}/pay", response_model=CapitalCallResponse)
def mark_capital_call_paid(
    fund_id: UUID,
    call_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    call = db.query(CapitalCall).filter(
        CapitalCall.id == call_id,
        CapitalCall.fund_id == fund_id,
        CapitalCall.deleted_at.is_(None)
    ).first()
    
    if not call:
        raise HTTPException(status_code=404, detail="Capital call not found")
    
    if call.is_paid:
        raise HTTPException(status_code=400, detail="Capital call already paid")
    
    call.is_paid = True
    call.payment_date = datetime.utcnow().date()
    
    # Update fund
    fund = db.query(PrivateFund).filter(PrivateFund.id == fund_id).first()
    fund.called_capital_amount += call.amount
    fund.uncalled_capital_amount = fund.committed_capital_amount - fund.called_capital_amount
    
    db.commit()
    db.refresh(call)
    return call


# Distributions
@router.get("/{fund_id}/distributions", response_model=List[DistributionResponse])
def list_distributions(
    fund_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dists = db.query(Distribution).filter(
        Distribution.fund_id == fund_id,
        Distribution.deleted_at.is_(None)
    ).order_by(Distribution.declaration_date.desc()).all()
    return dists


@router.post("/{fund_id}/distributions", response_model=DistributionResponse, status_code=status.HTTP_201_CREATED)
def create_distribution(
    fund_id: UUID,
    dist_in: DistributionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fund = db.query(PrivateFund).filter(
        PrivateFund.id == fund_id,
        PrivateFund.deleted_at.is_(None)
    ).first()
    
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    
    dist = Distribution(fund_id=fund_id, **dist_in.model_dump(exclude={"fund_id"}))
    db.add(dist)
    
    fund.distributions_declared += dist.amount
    
    db.commit()
    db.refresh(dist)
    return dist


@router.put("/{fund_id}/distributions/{dist_id}/receive", response_model=DistributionResponse)
def mark_distribution_received(
    fund_id: UUID,
    dist_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dist = db.query(Distribution).filter(
        Distribution.id == dist_id,
        Distribution.fund_id == fund_id,
        Distribution.deleted_at.is_(None)
    ).first()
    
    if not dist:
        raise HTTPException(status_code=404, detail="Distribution not found")
    
    if dist.is_received:
        raise HTTPException(status_code=400, detail="Distribution already received")
    
    dist.is_received = True
    dist.payment_date = datetime.utcnow().date()
    
    fund = db.query(PrivateFund).filter(PrivateFund.id == fund_id).first()
    fund.distributions_received += dist.amount
    
    db.commit()
    db.refresh(dist)
    return dist
