"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2025-01-16

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('username', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'cfo', 'ic_member', 'accountant', 'viewer', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_username', 'users', ['username'])
    
    # Audit logs
    op.create_table('audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('entity_type', sa.String(100), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('old_values', postgresql.JSONB(), nullable=True),
        sa.Column('new_values', postgresql.JSONB(), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Exchange rates
    op.create_table('exchange_rates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('from_currency', sa.String(3), nullable=False),
        sa.Column('to_currency', sa.String(3), nullable=False),
        sa.Column('rate_date', sa.Date(), nullable=False),
        sa.Column('rate', sa.BigInteger(), nullable=False),
        sa.Column('source', sa.String(100), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('from_currency', 'to_currency', 'rate_date', name='uq_exchange_rate')
    )
    op.create_index('ix_exchange_rates_from_currency', 'exchange_rates', ['from_currency'])
    op.create_index('ix_exchange_rates_to_currency', 'exchange_rates', ['to_currency'])
    op.create_index('ix_exchange_rates_rate_date', 'exchange_rates', ['rate_date'])
    
    # Equity holdings
    op.create_table('equity_holdings',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('ticker', sa.String(20), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('exchange', sa.Enum('NYSE', 'NASDAQ', 'LSE', 'BOURSA_KUWAIT', 'TADAWUL', 'DFM', 'ADX', 'QSE', 'BAHRAIN', 'MUSCAT', 'EGX', 'EURONEXT', 'HKEX', 'TSE', 'OTHER', name='exchange'), nullable=False),
        sa.Column('sector', sa.String(100), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('quantity', sa.BigInteger(), nullable=False, default=0),
        sa.Column('cost_basis_amount', sa.BigInteger(), nullable=False),
        sa.Column('cost_basis_currency', sa.String(3), nullable=False, default='KWD'),
        sa.Column('current_price_amount', sa.BigInteger(), nullable=True),
        sa.Column('current_price_currency', sa.String(3), default='USD'),
        sa.Column('current_value_kwd', sa.BigInteger(), nullable=True),
        sa.Column('realized_gain_loss', sa.BigInteger(), default=0),
        sa.Column('unrealized_gain_loss', sa.BigInteger(), default=0),
        sa.Column('status', sa.Enum('open', 'closed', 'partial', name='holdingstatus'), default='open'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_equity_holdings_ticker', 'equity_holdings', ['ticker'])
    
    # Equity transactions
    op.create_table('equity_transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('holding_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('transaction_type', sa.String(10), nullable=False),
        sa.Column('quantity', sa.BigInteger(), nullable=False),
        sa.Column('price_amount', sa.BigInteger(), nullable=False),
        sa.Column('price_currency', sa.String(3), nullable=False),
        sa.Column('total_amount', sa.BigInteger(), nullable=False),
        sa.Column('total_amount_kwd', sa.BigInteger(), nullable=False),
        sa.Column('transaction_date', sa.Date(), nullable=False),
        sa.Column('fees_amount', sa.BigInteger(), default=0),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['holding_id'], ['equity_holdings.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Dividends
    op.create_table('dividends',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('holding_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('amount', sa.BigInteger(), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False),
        sa.Column('amount_kwd', sa.BigInteger(), nullable=False),
        sa.Column('ex_date', sa.Date(), nullable=False),
        sa.Column('payment_date', sa.Date(), nullable=True),
        sa.Column('dividend_type', sa.String(50), nullable=True),
        sa.ForeignKeyConstraint(['holding_id'], ['equity_holdings.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Corporate actions
    op.create_table('corporate_actions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('holding_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('action_type', sa.Enum('bonus_shares', 'rights_issue', 'stock_split', 'reverse_split', 'spinoff', name='corporateactiontype'), nullable=False),
        sa.Column('action_date', sa.Date(), nullable=False),
        sa.Column('ratio_from', sa.BigInteger(), nullable=True),
        sa.Column('ratio_to', sa.BigInteger(), nullable=True),
        sa.Column('shares_received', sa.BigInteger(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['holding_id'], ['equity_holdings.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Fixed income holdings
    op.create_table('fixed_income_holdings',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('isin', sa.String(20), nullable=True),
        sa.Column('instrument_type', sa.Enum('corporate_bond', 'government_bond', 'sukuk', 'fixed_income_fund', 'treasury', name='fixedincometype'), nullable=False),
        sa.Column('issuer', sa.String(255), nullable=True),
        sa.Column('face_value_amount', sa.BigInteger(), nullable=False),
        sa.Column('face_value_currency', sa.String(3), nullable=False, default='USD'),
        sa.Column('purchase_price_amount', sa.BigInteger(), nullable=False),
        sa.Column('purchase_price_currency', sa.String(3), nullable=False),
        sa.Column('purchase_date', sa.Date(), nullable=False),
        sa.Column('coupon_rate', sa.Integer(), nullable=True),
        sa.Column('coupon_frequency', sa.String(20), nullable=True),
        sa.Column('maturity_date', sa.Date(), nullable=True),
        sa.Column('current_market_value_amount', sa.BigInteger(), nullable=True),
        sa.Column('current_market_value_currency', sa.String(3), nullable=True),
        sa.Column('current_value_kwd', sa.BigInteger(), nullable=True),
        sa.Column('irr_bps', sa.Integer(), nullable=True),
        sa.Column('expected_return_bps', sa.Integer(), nullable=True),
        sa.Column('management_fee_bps', sa.Integer(), nullable=True),
        sa.Column('is_exchange_traded', sa.String(10), default='no'),
        sa.Column('status', sa.Enum('active', 'matured', 'sold', 'defaulted', name='fixedincomestatus'), default='active'),
        sa.Column('accrued_interest', sa.BigInteger(), default=0),
        sa.Column('total_interest_received', sa.BigInteger(), default=0),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_fixed_income_holdings_isin', 'fixed_income_holdings', ['isin'])
    
    # Properties
    op.create_table('properties',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('property_type', sa.Enum('commercial', 'residential', 'mixed', 'land', 'industrial', name='propertytype'), nullable=False),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('country', sa.String(100), default='Kuwait'),
        sa.Column('purchase_price_amount', sa.BigInteger(), nullable=False),
        sa.Column('purchase_price_currency', sa.String(3), default='KWD'),
        sa.Column('purchase_date', sa.Date(), nullable=False),
        sa.Column('current_value_amount', sa.BigInteger(), nullable=True),
        sa.Column('current_value_currency', sa.String(3), default='KWD'),
        sa.Column('last_valuation_date', sa.Date(), nullable=True),
        sa.Column('ownership_entity', sa.String(255), nullable=True),
        sa.Column('ownership_percentage', sa.Integer(), default=10000),
        sa.Column('total_area_sqm', sa.BigInteger(), nullable=True),
        sa.Column('irr_bps', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Units
    op.create_table('units',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('property_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('unit_number', sa.String(50), nullable=False),
        sa.Column('unit_type', sa.String(50), nullable=True),
        sa.Column('floor', sa.Integer(), nullable=True),
        sa.Column('area_sqm', sa.BigInteger(), nullable=True),
        sa.Column('status', sa.Enum('occupied', 'vacant', 'under_maintenance', 'reserved', name='unitstatus'), default='vacant'),
        sa.Column('tenant_name', sa.String(255), nullable=True),
        sa.Column('lease_start_date', sa.Date(), nullable=True),
        sa.Column('lease_end_date', sa.Date(), nullable=True),
        sa.Column('monthly_rent_amount', sa.BigInteger(), nullable=True),
        sa.Column('monthly_rent_currency', sa.String(3), default='KWD'),
        sa.Column('budgeted_rent_amount', sa.BigInteger(), nullable=True),
        sa.Column('deposit_amount', sa.BigInteger(), default=0),
        sa.Column('outstanding_amount', sa.BigInteger(), default=0),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Rental income
    op.create_table('rental_income',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('unit_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('period_start', sa.Date(), nullable=False),
        sa.Column('period_end', sa.Date(), nullable=False),
        sa.Column('expected_amount', sa.BigInteger(), nullable=False),
        sa.Column('received_amount', sa.BigInteger(), default=0),
        sa.Column('currency', sa.String(3), default='KWD'),
        sa.Column('payment_date', sa.Date(), nullable=True),
        sa.Column('is_collected', sa.Boolean(), default=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['unit_id'], ['units.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Property expenses
    op.create_table('property_expenses',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('property_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('unit_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('expense_type', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('amount', sa.BigInteger(), nullable=False),
        sa.Column('currency', sa.String(3), default='KWD'),
        sa.Column('expense_date', sa.Date(), nullable=False),
        sa.Column('vendor_name', sa.String(255), nullable=True),
        sa.Column('invoice_number', sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id']),
        sa.ForeignKeyConstraint(['unit_id'], ['units.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Property valuations
    op.create_table('property_valuations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('property_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('valuation_date', sa.Date(), nullable=False),
        sa.Column('value_amount', sa.BigInteger(), nullable=False),
        sa.Column('currency', sa.String(3), default='KWD'),
        sa.Column('appraiser', sa.String(255), nullable=True),
        sa.Column('valuation_method', sa.String(100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Private funds
    op.create_table('private_funds',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('fund_type', sa.Enum('private_equity', 'venture_capital', 'hedge_fund', 'real_estate_fund', 'infrastructure', 'direct_investment', 'co_investment', name='fundtype'), nullable=False),
        sa.Column('fund_manager', sa.String(255), nullable=True),
        sa.Column('vintage_year', sa.Integer(), nullable=True),
        sa.Column('geography', sa.String(100), nullable=True),
        sa.Column('sector', sa.String(100), nullable=True),
        sa.Column('committed_capital_amount', sa.BigInteger(), nullable=False),
        sa.Column('committed_capital_currency', sa.String(3), default='USD'),
        sa.Column('called_capital_amount', sa.BigInteger(), default=0),
        sa.Column('uncalled_capital_amount', sa.BigInteger(), nullable=True),
        sa.Column('distributions_declared', sa.BigInteger(), default=0),
        sa.Column('distributions_received', sa.BigInteger(), default=0),
        sa.Column('current_nav_amount', sa.BigInteger(), nullable=True),
        sa.Column('current_nav_currency', sa.String(3), default='USD'),
        sa.Column('current_nav_kwd', sa.BigInteger(), nullable=True),
        sa.Column('nav_date', sa.Date(), nullable=True),
        sa.Column('irr_bps', sa.Integer(), nullable=True),
        sa.Column('tvpi_bps', sa.Integer(), nullable=True),
        sa.Column('dpi_bps', sa.Integer(), nullable=True),
        sa.Column('management_fee_bps', sa.Integer(), nullable=True),
        sa.Column('carried_interest_bps', sa.Integer(), nullable=True),
        sa.Column('fund_term_years', sa.Integer(), nullable=True),
        sa.Column('investment_period_end', sa.Date(), nullable=True),
        sa.Column('fund_end_date', sa.Date(), nullable=True),
        sa.Column('status', sa.Enum('active', 'fully_realized', 'partially_realized', 'written_off', name='fundstatus'), default='active'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Capital calls
    op.create_table('capital_calls',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('fund_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('call_number', sa.Integer(), nullable=True),
        sa.Column('call_date', sa.Date(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('payment_date', sa.Date(), nullable=True),
        sa.Column('amount', sa.BigInteger(), nullable=False),
        sa.Column('currency', sa.String(3), default='USD'),
        sa.Column('amount_kwd', sa.BigInteger(), nullable=True),
        sa.Column('purpose', sa.String(255), nullable=True),
        sa.Column('is_paid', sa.Boolean(), default=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['fund_id'], ['private_funds.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Distributions
    op.create_table('distributions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('fund_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('distribution_number', sa.Integer(), nullable=True),
        sa.Column('declaration_date', sa.Date(), nullable=False),
        sa.Column('payment_date', sa.Date(), nullable=True),
        sa.Column('amount', sa.BigInteger(), nullable=False),
        sa.Column('currency', sa.String(3), default='USD'),
        sa.Column('amount_kwd', sa.BigInteger(), nullable=True),
        sa.Column('distribution_type', sa.String(50), nullable=True),
        sa.Column('is_received', sa.Boolean(), default=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['fund_id'], ['private_funds.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Fund valuations
    op.create_table('fund_valuations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('fund_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('valuation_date', sa.Date(), nullable=False),
        sa.Column('nav_amount', sa.BigInteger(), nullable=False),
        sa.Column('currency', sa.String(3), default='USD'),
        sa.Column('nav_kwd', sa.BigInteger(), nullable=True),
        sa.Column('irr_bps', sa.Integer(), nullable=True),
        sa.Column('tvpi_bps', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['fund_id'], ['private_funds.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('fund_valuations')
    op.drop_table('distributions')
    op.drop_table('capital_calls')
    op.drop_table('private_funds')
    op.drop_table('property_valuations')
    op.drop_table('property_expenses')
    op.drop_table('rental_income')
    op.drop_table('units')
    op.drop_table('properties')
    op.drop_table('fixed_income_holdings')
    op.drop_table('corporate_actions')
    op.drop_table('dividends')
    op.drop_table('equity_transactions')
    op.drop_table('equity_holdings')
    op.drop_table('exchange_rates')
    op.drop_table('audit_logs')
    op.drop_table('users')
    
    op.execute('DROP TYPE IF EXISTS fundstatus')
    op.execute('DROP TYPE IF EXISTS fundtype')
    op.execute('DROP TYPE IF EXISTS unitstatus')
    op.execute('DROP TYPE IF EXISTS propertytype')
    op.execute('DROP TYPE IF EXISTS fixedincomestatus')
    op.execute('DROP TYPE IF EXISTS fixedincometype')
    op.execute('DROP TYPE IF EXISTS corporateactiontype')
    op.execute('DROP TYPE IF EXISTS holdingstatus')
    op.execute('DROP TYPE IF EXISTS exchange')
    op.execute('DROP TYPE IF EXISTS userrole')
