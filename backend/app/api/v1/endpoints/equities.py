from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.core.database import get_db
from app.models.user import User
from app.models.equity import EquityHolding, EquityTransaction, Dividend, CorporateAction
from app.schemas.equity import (
    EquityHoldingCreate, EquityHoldingUpdate, EquityHoldingResponse,
    EquityTransactionCreate, EquityTransactionResponse,
    DividendCreate, DividendResponse,
    CorporateActionCreate, CorporateActionResponse
)
from app.schemas.common import PaginatedResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("", response_model=PaginatedResponse[EquityHoldingResponse])
def list_equities(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    exchange: Optional[str] = None,
    sector: Optional[str] = None,
    country: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(EquityHolding).filter(EquityHolding.deleted_at.is_(None))
    
    if exchange:
        query = query.filter(EquityHolding.exchange == exchange)
    if sector:
        query = query.filter(EquityHolding.sector == sector)
    if country:
        query = query.filter(EquityHolding.country == country)
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.post("", response_model=EquityHoldingResponse, status_code=status.HTTP_201_CREATED)
def create_equity(
    holding_in: EquityHoldingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    holding = EquityHolding(**holding_in.model_dump())
    db.add(holding)
    db.commit()
    db.refresh(holding)
    return holding


@router.get("/{holding_id}", response_model=EquityHoldingResponse)
def get_equity(
    holding_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    holding = db.query(EquityHolding).filter(
        EquityHolding.id == holding_id,
        EquityHolding.deleted_at.is_(None)
    ).first()
    
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    return holding


@router.put("/{holding_id}", response_model=EquityHoldingResponse)
def update_equity(
    holding_id: UUID,
    holding_in: EquityHoldingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    holding = db.query(EquityHolding).filter(
        EquityHolding.id == holding_id,
        EquityHolding.deleted_at.is_(None)
    ).first()
    
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    
    for field, value in holding_in.model_dump(exclude_unset=True).items():
        setattr(holding, field, value)
    
    db.commit()
    db.refresh(holding)
    return holding


@router.delete("/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equity(
    holding_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    holding = db.query(EquityHolding).filter(
        EquityHolding.id == holding_id,
        EquityHolding.deleted_at.is_(None)
    ).first()
    
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    
    holding.deleted_at = datetime.utcnow()
    db.commit()


# Transactions
@router.get("/{holding_id}/transactions", response_model=List[EquityTransactionResponse])
def list_transactions(
    holding_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transactions = db.query(EquityTransaction).filter(
        EquityTransaction.holding_id == holding_id,
        EquityTransaction.deleted_at.is_(None)
    ).order_by(EquityTransaction.transaction_date.desc()).all()
    return transactions


@router.post("/{holding_id}/transactions", response_model=EquityTransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    holding_id: UUID,
    tx_in: EquityTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    holding = db.query(EquityHolding).filter(
        EquityHolding.id == holding_id,
        EquityHolding.deleted_at.is_(None)
    ).first()
    
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    
    total_amount = tx_in.quantity * tx_in.price_amount + tx_in.fees_amount
    
    tx = EquityTransaction(
        holding_id=holding_id,
        transaction_type=tx_in.transaction_type,
        quantity=tx_in.quantity,
        price_amount=tx_in.price_amount,
        price_currency=tx_in.price_currency,
        total_amount=total_amount,
        total_amount_kwd=total_amount,  # TODO: Convert currency
        transaction_date=tx_in.transaction_date,
        fees_amount=tx_in.fees_amount,
        notes=tx_in.notes
    )
    db.add(tx)
    
    # Update holding quantity
    if tx_in.transaction_type == "BUY":
        holding.quantity += tx_in.quantity
    else:
        holding.quantity -= tx_in.quantity
    
    db.commit()
    db.refresh(tx)
    return tx


# Dividends
@router.get("/{holding_id}/dividends", response_model=List[DividendResponse])
def list_dividends(
    holding_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dividends = db.query(Dividend).filter(
        Dividend.holding_id == holding_id,
        Dividend.deleted_at.is_(None)
    ).order_by(Dividend.ex_date.desc()).all()
    return dividends


@router.post("/{holding_id}/dividends", response_model=DividendResponse, status_code=status.HTTP_201_CREATED)
def create_dividend(
    holding_id: UUID,
    div_in: DividendCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    holding = db.query(EquityHolding).filter(
        EquityHolding.id == holding_id,
        EquityHolding.deleted_at.is_(None)
    ).first()
    
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    
    dividend = Dividend(
        holding_id=holding_id,
        amount=div_in.amount,
        currency=div_in.currency,
        amount_kwd=div_in.amount,  # TODO: Convert
        ex_date=div_in.ex_date,
        payment_date=div_in.payment_date,
        dividend_type=div_in.dividend_type
    )
    db.add(dividend)
    db.commit()
    db.refresh(dividend)
    return dividend
