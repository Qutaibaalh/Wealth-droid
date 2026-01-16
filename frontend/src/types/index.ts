export interface User {
  id: string;
  username: string;
  email: string;
  full_name: string;
  role: 'admin' | 'cfo' | 'ic_member' | 'accountant' | 'viewer';
  is_active: boolean;
  created_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface AllocationItem {
  category: string;
  value_kwd: number;
  percentage: number;
  color?: string;
}

export interface AssetClassSummary {
  asset_class: string;
  total_value_kwd: number;
  cost_basis_kwd: number;
  unrealized_gain_loss: number;
  realized_gain_loss: number;
  income_received: number;
  irr_bps?: number;
  holdings_count: number;
}

export interface PortfolioSummary {
  total_value_kwd: number;
  total_cost_basis_kwd: number;
  total_unrealized_gain_loss: number;
  total_realized_gain_loss: number;
  total_income_kwd: number;
  portfolio_irr_bps?: number;
  asset_class_breakdown: AssetClassSummary[];
  allocation: AllocationItem[];
  equities_count: number;
  fixed_income_count: number;
  properties_count: number;
  units_count: number;
  private_funds_count: number;
  as_of_date: string;
}

export interface EquityHolding {
  id: string;
  ticker: string;
  name: string;
  exchange: string;
  sector?: string;
  country?: string;
  quantity: number;
  cost_basis_amount: number;
  cost_basis_currency: string;
  current_price_amount?: number;
  current_price_currency?: string;
  current_value_kwd?: number;
  realized_gain_loss: number;
  unrealized_gain_loss: number;
  status: 'open' | 'closed' | 'partial';
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface FixedIncomeHolding {
  id: string;
  name: string;
  isin?: string;
  instrument_type: string;
  issuer?: string;
  face_value_amount: number;
  face_value_currency: string;
  purchase_price_amount: number;
  purchase_price_currency: string;
  purchase_date: string;
  coupon_rate?: number;
  coupon_frequency?: string;
  maturity_date?: string;
  current_market_value_amount?: number;
  current_value_kwd?: number;
  irr_bps?: number;
  expected_return_bps?: number;
  status: string;
  created_at: string;
}

export interface Property {
  id: string;
  name: string;
  property_type: string;
  address?: string;
  city?: string;
  country: string;
  purchase_price_amount: number;
  purchase_price_currency: string;
  purchase_date: string;
  current_value_amount?: number;
  current_value_currency?: string;
  ownership_entity?: string;
  ownership_percentage: number;
  irr_bps?: number;
  units: Unit[];
  created_at: string;
}

export interface Unit {
  id: string;
  property_id: string;
  unit_number: string;
  unit_type?: string;
  floor?: number;
  status: 'occupied' | 'vacant' | 'under_maintenance' | 'reserved';
  tenant_name?: string;
  monthly_rent_amount?: number;
  monthly_rent_currency: string;
  outstanding_amount: number;
}

export interface OccupancyReport {
  property_id: string;
  property_name: string;
  total_units: number;
  occupied_units: number;
  vacant_units: number;
  occupancy_rate: number;
  total_monthly_rent: number;
  total_collected: number;
  total_outstanding: number;
  currency: string;
}

export interface PrivateFund {
  id: string;
  name: string;
  fund_type: string;
  fund_manager?: string;
  vintage_year?: number;
  geography?: string;
  sector?: string;
  committed_capital_amount: number;
  committed_capital_currency: string;
  called_capital_amount: number;
  uncalled_capital_amount?: number;
  distributions_declared: number;
  distributions_received: number;
  current_nav_amount?: number;
  current_nav_kwd?: number;
  irr_bps?: number;
  tvpi_bps?: number;
  dpi_bps?: number;
  management_fee_bps?: number;
  carried_interest_bps?: number;
  fund_term_years?: number;
  status: string;
  created_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface ExposureBreakdown {
  dimension: string;
  items: AllocationItem[];
}
