import axios from 'axios';
import type { 
  Token, 
  User, 
  PortfolioSummary, 
  EquityHolding, 
  FixedIncomeHolding,
  Property,
  PrivateFund,
  OccupancyReport,
  PaginatedResponse,
  ExposureBreakdown
} from '../types';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth
export const login = async (username: string, password: string): Promise<Token> => {
  const { data } = await api.post<Token>('/auth/login', { username, password });
  return data;
};

export const getCurrentUser = async (): Promise<User> => {
  const { data } = await api.get<User>('/auth/me');
  return data;
};

export const logout = async (): Promise<void> => {
  await api.post('/auth/logout');
};

// Portfolio
export const getPortfolioSummary = async (): Promise<PortfolioSummary> => {
  const { data } = await api.get<PortfolioSummary>('/portfolio/summary');
  return data;
};

export const getGeographyExposure = async (): Promise<ExposureBreakdown> => {
  const { data } = await api.get<ExposureBreakdown>('/portfolio/exposure/geography');
  return data;
};

export const getCurrencyExposure = async (): Promise<ExposureBreakdown> => {
  const { data } = await api.get<ExposureBreakdown>('/portfolio/exposure/currency');
  return data;
};

export const getSectorExposure = async (): Promise<ExposureBreakdown> => {
  const { data } = await api.get<ExposureBreakdown>('/portfolio/exposure/sector');
  return data;
};

// Equities
export const getEquities = async (page = 1, size = 50): Promise<PaginatedResponse<EquityHolding>> => {
  const { data } = await api.get<PaginatedResponse<EquityHolding>>('/holdings/equities', {
    params: { page, size }
  });
  return data;
};

export const getEquity = async (id: string): Promise<EquityHolding> => {
  const { data } = await api.get<EquityHolding>(`/holdings/equities/${id}`);
  return data;
};

export const createEquity = async (holding: Partial<EquityHolding>): Promise<EquityHolding> => {
  const { data } = await api.post<EquityHolding>('/holdings/equities', holding);
  return data;
};

export const updateEquity = async (id: string, holding: Partial<EquityHolding>): Promise<EquityHolding> => {
  const { data } = await api.put<EquityHolding>(`/holdings/equities/${id}`, holding);
  return data;
};

export const deleteEquity = async (id: string): Promise<void> => {
  await api.delete(`/holdings/equities/${id}`);
};

// Fixed Income
export const getFixedIncome = async (page = 1, size = 50): Promise<PaginatedResponse<FixedIncomeHolding>> => {
  const { data } = await api.get<PaginatedResponse<FixedIncomeHolding>>('/holdings/fixed-income', {
    params: { page, size }
  });
  return data;
};

export const getFixedIncomeById = async (id: string): Promise<FixedIncomeHolding> => {
  const { data } = await api.get<FixedIncomeHolding>(`/holdings/fixed-income/${id}`);
  return data;
};

export const createFixedIncome = async (holding: Partial<FixedIncomeHolding>): Promise<FixedIncomeHolding> => {
  const { data } = await api.post<FixedIncomeHolding>('/holdings/fixed-income', holding);
  return data;
};

export const updateFixedIncome = async (id: string, holding: Partial<FixedIncomeHolding>): Promise<FixedIncomeHolding> => {
  const { data } = await api.put<FixedIncomeHolding>(`/holdings/fixed-income/${id}`, holding);
  return data;
};

export const deleteFixedIncome = async (id: string): Promise<void> => {
  await api.delete(`/holdings/fixed-income/${id}`);
};

// Real Estate
export const getProperties = async (page = 1, size = 50): Promise<PaginatedResponse<Property>> => {
  const { data } = await api.get<PaginatedResponse<Property>>('/real-estate/properties', {
    params: { page, size }
  });
  return data;
};

export const getProperty = async (id: string): Promise<Property> => {
  const { data } = await api.get<Property>(`/real-estate/properties/${id}`);
  return data;
};

export const createProperty = async (property: Partial<Property>): Promise<Property> => {
  const { data } = await api.post<Property>('/real-estate/properties', property);
  return data;
};

export const updateProperty = async (id: string, property: Partial<Property>): Promise<Property> => {
  const { data } = await api.put<Property>(`/real-estate/properties/${id}`, property);
  return data;
};

export const deleteProperty = async (id: string): Promise<void> => {
  await api.delete(`/real-estate/properties/${id}`);
};

export const getOccupancyReport = async (): Promise<OccupancyReport[]> => {
  const { data } = await api.get<OccupancyReport[]>('/real-estate/occupancy-report');
  return data;
};

// Private Funds
export const getPrivateFunds = async (page = 1, size = 50): Promise<PaginatedResponse<PrivateFund>> => {
  const { data } = await api.get<PaginatedResponse<PrivateFund>>('/private-funds', {
    params: { page, size }
  });
  return data;
};

export const getPrivateFund = async (id: string): Promise<PrivateFund> => {
  const { data } = await api.get<PrivateFund>(`/private-funds/${id}`);
  return data;
};

export const createPrivateFund = async (fund: Partial<PrivateFund>): Promise<PrivateFund> => {
  const { data } = await api.post<PrivateFund>('/private-funds', fund);
  return data;
};

export const updatePrivateFund = async (id: string, fund: Partial<PrivateFund>): Promise<PrivateFund> => {
  const { data } = await api.put<PrivateFund>(`/private-funds/${id}`, fund);
  return data;
};

export const deletePrivateFund = async (id: string): Promise<void> => {
  await api.delete(`/private-funds/${id}`);
};

// Reports
export const downloadReport = async (type: string): Promise<void> => {
  const response = await api.get(`/reports/pdf?report_type=${type}`, {
    responseType: 'blob'
  });
  
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `portfolio_report_${type}.pdf`);
  document.body.appendChild(link);
  link.click();
  link.remove();
};

export default api;
