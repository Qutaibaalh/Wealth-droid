export function formatMoney(amount: number, currency = 'KWD'): string {
  const divisor = currency === 'KWD' ? 1000 : 100;
  const decimals = currency === 'KWD' ? 3 : 2;
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(amount / divisor);
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat('en-US').format(value);
}

export function formatPercent(value: number): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
}

export function formatBps(bps: number): string {
  return `${(bps / 100).toFixed(2)}%`;
}

export function formatCompactMoney(amount: number, currency = 'KWD'): string {
  const divisor = currency === 'KWD' ? 1000 : 100;
  const value = amount / divisor;
  
  if (value >= 1000000) {
    return `${(value / 1000000).toFixed(2)}M ${currency}`;
  }
  if (value >= 1000) {
    return `${(value / 1000).toFixed(2)}K ${currency}`;
  }
  return formatMoney(amount, currency);
}

export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

export function getGainLossColor(value: number): string {
  if (value > 0) return 'text-emerald-400';
  if (value < 0) return 'text-rose-400';
  return 'text-brand-400';
}

export function getStatusColor(status: string): string {
  switch (status.toLowerCase()) {
    case 'active':
    case 'open':
    case 'occupied':
      return 'badge-success';
    case 'pending':
    case 'partial':
    case 'reserved':
      return 'badge-warning';
    case 'closed':
    case 'vacant':
    case 'matured':
      return 'badge-info';
    case 'defaulted':
    case 'written_off':
    case 'under_maintenance':
      return 'badge-danger';
    default:
      return 'badge-info';
  }
}
