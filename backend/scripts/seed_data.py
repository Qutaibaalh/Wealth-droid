"""Seed initial data including admin user and sample investments."""
import sys
sys.path.insert(0, '.')

from sqlalchemy import text
from app.core.database import SessionLocal
from app.core.security import get_password_hash
import uuid
from datetime import datetime

def seed():
    db = SessionLocal()
    now = datetime.utcnow()
    
    # Create users
    result = db.execute(text("SELECT id FROM users WHERE username = 'admin'")).first()
    if not result:
        admin_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO users (id, username, email, hashed_password, full_name, role, is_active, created_at, updated_at)
            VALUES (:id, :username, :email, :hashed_password, :full_name, :role, :is_active, :created_at, :updated_at)
        """), {
            "id": admin_id,
            "username": "admin",
            "email": "admin@alrashid.com",
            "hashed_password": get_password_hash("admin123"),
            "full_name": "System Administrator",
            "role": "admin",
            "is_active": True,
            "created_at": now,
            "updated_at": now
        })
        print("Created admin user: admin / admin123")
    
    result = db.execute(text("SELECT id FROM users WHERE username = 'cfo'")).first()
    if not result:
        cfo_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO users (id, username, email, hashed_password, full_name, role, is_active, created_at, updated_at)
            VALUES (:id, :username, :email, :hashed_password, :full_name, :role, :is_active, :created_at, :updated_at)
        """), {
            "id": cfo_id,
            "username": "cfo",
            "email": "cfo@alrashid.com",
            "hashed_password": get_password_hash("cfo123"),
            "full_name": "Chief Financial Officer",
            "role": "cfo",
            "is_active": True,
            "created_at": now,
            "updated_at": now
        })
        print("Created CFO user: cfo / cfo123")
    
    result = db.execute(text("SELECT id FROM users WHERE username = 'ic_member'")).first()
    if not result:
        ic_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO users (id, username, email, hashed_password, full_name, role, is_active, created_at, updated_at)
            VALUES (:id, :username, :email, :hashed_password, :full_name, :role, :is_active, :created_at, :updated_at)
        """), {
            "id": ic_id,
            "username": "ic_member",
            "email": "ic@alrashid.com",
            "hashed_password": get_password_hash("ic123"),
            "full_name": "Investment Committee Member",
            "role": "ic_member",
            "is_active": True,
            "created_at": now,
            "updated_at": now
        })
        print("Created IC member user: ic_member / ic123")
    
    # Seed sample equity
    result = db.execute(text("SELECT id FROM equity_holdings WHERE ticker = 'AAPL'")).first()
    if not result:
        equity_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO equity_holdings (id, ticker, name, exchange, sector, country, quantity, cost_basis_amount, cost_basis_currency, 
                                        current_price_amount, current_price_currency, current_value_kwd, status, created_at, updated_at)
            VALUES (:id, :ticker, :name, :exchange, :sector, :country, :quantity, :cost_basis_amount, :cost_basis_currency,
                   :current_price_amount, :current_price_currency, :current_value_kwd, :status, :created_at, :updated_at)
        """), {
            "id": equity_id,
            "ticker": "AAPL",
            "name": "Apple Inc.",
            "exchange": "NASDAQ",
            "sector": "Technology",
            "country": "USA",
            "quantity": 100,
            "cost_basis_amount": 15000000,  # 150 per share * 100,000 (cents)
            "cost_basis_currency": "USD",
            "current_price_amount": 19000000,  # 190 per share
            "current_price_currency": "USD",
            "current_value_kwd": 58300000,  # 58.3M KWD
            "status": "open",
            "created_at": now,
            "updated_at": now
        })
        print("Created sample Equity: AAPL")
    
    # Seed sample fixed income
    result = db.execute(text("SELECT id FROM fixed_income_holdings WHERE name = 'Corporate Bond 5%'")).first()
    if not result:
        fi_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO fixed_income_holdings (id, name, instrument_type, issuer, face_value_amount, face_value_currency,
                                              purchase_price_amount, purchase_price_currency, purchase_date, coupon_rate,
                                              coupon_frequency, maturity_date, current_value_kwd, status, created_at, updated_at)
            VALUES (:id, :name, :instrument_type, :issuer, :face_value_amount, :face_value_currency,
                   :purchase_price_amount, :purchase_price_currency, :purchase_date, :coupon_rate,
                   :coupon_frequency, :maturity_date, :current_value_kwd, :status, :created_at, :updated_at)
        """), {
            "id": fi_id,
            "name": "Corporate Bond 5%",
            "instrument_type": "corporate_bond",
            "issuer": "Kuwait Finance House",
            "face_value_amount": 10000000,  # 100k USD
            "face_value_currency": "USD",
            "purchase_price_amount": 10000000,
            "purchase_price_currency": "USD",
            "purchase_date": "2023-01-15",
            "coupon_rate": 500,  # 5%
            "coupon_frequency": "annual",
            "maturity_date": "2030-01-15",
            "current_value_kwd": 3070000,  # ~30.7k KWD
            "status": "active",
            "created_at": now,
            "updated_at": now
        })
        print("Created sample Fixed Income: Corporate Bond")
    
    # Seed sample property
    result = db.execute(text("SELECT id FROM properties WHERE name = 'Marina Commercial Tower'")).first()
    if not result:
        prop_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO properties (id, name, property_type, address, city, country, purchase_price_amount, purchase_price_currency,
                                   purchase_date, ownership_entity, ownership_percentage, created_at, updated_at)
            VALUES (:id, :name, :property_type, :address, :city, :country, :purchase_price_amount, :purchase_price_currency,
                   :purchase_date, :ownership_entity, :ownership_percentage, :created_at, :updated_at)
        """), {
            "id": prop_id,
            "name": "Marina Commercial Tower",
            "property_type": "commercial",
            "address": "Building A, Marina Complex",
            "city": "Kuwait City",
            "country": "Kuwait",
            "purchase_price_amount": 50000000000,  # 500M KWD
            "purchase_price_currency": "KWD",
            "purchase_date": "2020-06-15",
            "ownership_entity": "AL Rashid Real Estate Co.",
            "ownership_percentage": 10000,  # 100%
            "created_at": now,
            "updated_at": now
        })
        print("Created sample Property: Marina Commercial Tower")
    
    # Seed sample private fund
    result = db.execute(text("SELECT id FROM private_funds WHERE name = 'Gulf PE Fund III'")).first()
    if not result:
        fund_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO private_funds (id, name, fund_type, fund_manager, vintage_year, geography, sector,
                                      committed_capital_amount, committed_capital_currency, called_capital_amount,
                                      uncalled_capital_amount, status, created_at, updated_at)
            VALUES (:id, :name, :fund_type, :fund_manager, :vintage_year, :geography, :sector,
                   :committed_capital_amount, :committed_capital_currency, :called_capital_amount,
                   :uncalled_capital_amount, :status, :created_at, :updated_at)
        """), {
            "id": fund_id,
            "name": "Gulf PE Fund III",
            "fund_type": "private_equity",
            "fund_manager": "Abraaj Capital",
            "vintage_year": 2021,
            "geography": "MENA",
            "sector": "Diversified",
            "committed_capital_amount": 50000000,  # 500M USD
            "committed_capital_currency": "USD",
            "called_capital_amount": 30000000,  # 300M USD
            "uncalled_capital_amount": 20000000,
            "status": "active",
            "created_at": now,
            "updated_at": now
        })
        print("Created sample Private Fund: Gulf PE Fund III")
    
    db.commit()
    db.close()
    print("Seed completed!")


if __name__ == "__main__":
    seed()
