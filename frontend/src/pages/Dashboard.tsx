import { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import { TrendingUp, TrendingDown, Building2, Briefcase, DollarSign } from 'lucide-react';
import { getPortfolioSummary, getGeographyExposure, getCurrencyExposure } from '../services/api';
import type { PortfolioSummary, ExposureBreakdown } from '../types';
import { formatMoney, formatCompactMoney, formatPercent, getGainLossColor } from '../utils/format';
import clsx from 'clsx';

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#06B6D4'];

function StatCard({ 
  title, 
  value, 
  subValue, 
  icon: Icon, 
  trend,
  delay 
}: { 
  title: string;
  value: string;
  subValue?: string;
  icon: React.ElementType;
  trend?: number;
  delay: number;
}) {
  return (
    <div 
      className={clsx(
        "card card-hover p-6 animate-slide-up opacity-0",
        `animate-delay-${delay}`
      )}
      style={{ animationFillMode: 'forwards' }}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="p-3 bg-brand-800/50 rounded-xl">
          <Icon className="w-6 h-6 text-gold-400" />
        </div>
        {trend !== undefined && (
          <div className={clsx(
            "flex items-center gap-1 text-sm font-medium",
            trend >= 0 ? "text-emerald-400" : "text-rose-400"
          )}>
            {trend >= 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
            {formatPercent(trend)}
          </div>
        )}
      </div>
      <p className="stat-label mb-1">{title}</p>
      <p className="stat-value">{value}</p>
      {subValue && (
        <p className="text-sm text-brand-400 mt-1">{subValue}</p>
      )}
    </div>
  );
}

export default function Dashboard() {
  const [summary, setSummary] = useState<PortfolioSummary | null>(null);
  const [geoExposure, setGeoExposure] = useState<ExposureBreakdown | null>(null);
  const [currExposure, setCurrExposure] = useState<ExposureBreakdown | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [summaryData, geoData, currData] = await Promise.all([
          getPortfolioSummary(),
          getGeographyExposure(),
          getCurrencyExposure(),
        ]);
        setSummary(summaryData);
        setGeoExposure(geoData);
        setCurrExposure(currData);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    }
    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-pulse text-gold-400">Loading dashboard...</div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="text-center text-brand-400 py-12">
        Failed to load dashboard data
      </div>
    );
  }

  const gainLossPercent = summary.total_cost_basis_kwd > 0
    ? ((summary.total_unrealized_gain_loss / summary.total_cost_basis_kwd) * 100)
    : 0;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="animate-fade-in">
        <h1 className="text-3xl font-display font-bold text-brand-50 mb-2">Portfolio Overview</h1>
        <p className="text-brand-400">
          As of {new Date(summary.as_of_date).toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })}
        </p>
      </div>

      {/* Key metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Portfolio Value"
          value={formatCompactMoney(summary.total_value_kwd)}
          subValue={`Cost: ${formatCompactMoney(summary.total_cost_basis_kwd)}`}
          icon={DollarSign}
          trend={gainLossPercent}
          delay={100}
        />
        <StatCard
          title="Unrealized Gain/Loss"
          value={formatCompactMoney(summary.total_unrealized_gain_loss)}
          icon={summary.total_unrealized_gain_loss >= 0 ? TrendingUp : TrendingDown}
          delay={200}
        />
        <StatCard
          title="Properties"
          value={summary.properties_count.toString()}
          subValue={`${summary.units_count} total units`}
          icon={Building2}
          delay={300}
        />
        <StatCard
          title="Private Funds"
          value={summary.private_funds_count.toString()}
          subValue={`${summary.equities_count} equities`}
          icon={Briefcase}
          delay={400}
        />
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Asset Allocation */}
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-brand-100 mb-6">Asset Allocation</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={summary.allocation}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="value_kwd"
                  nameKey="category"
                >
                  {summary.allocation.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color || COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value: number) => formatMoney(value)}
                  contentStyle={{
                    backgroundColor: '#1e3a5f',
                    border: '1px solid #334e68',
                    borderRadius: '8px',
                    color: '#e2e8f0'
                  }}
                />
                <Legend
                  formatter={(value) => <span className="text-brand-200">{value}</span>}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Asset Class Performance */}
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-brand-100 mb-6">Asset Class Summary</h2>
          <div className="space-y-4">
            {summary.asset_class_breakdown.map((item) => {
              const gainLoss = item.unrealized_gain_loss;
              const gainLossPercent = item.cost_basis_kwd > 0
                ? (gainLoss / item.cost_basis_kwd) * 100
                : 0;
              
              return (
                <div key={item.asset_class} className="flex items-center justify-between py-3 border-b border-brand-800/50 last:border-0">
                  <div>
                    <p className="font-medium text-brand-100">{item.asset_class}</p>
                    <p className="text-sm text-brand-400">{item.holdings_count} holdings</p>
                  </div>
                  <div className="text-right">
                    <p className="font-mono font-medium text-brand-100">
                      {formatCompactMoney(item.total_value_kwd)}
                    </p>
                    <p className={clsx("text-sm font-mono", getGainLossColor(gainLoss))}>
                      {formatPercent(gainLossPercent)}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Exposure breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Geography */}
        {geoExposure && geoExposure.items.length > 0 && (
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-brand-100 mb-6">Geographic Exposure</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={geoExposure.items.slice(0, 6)} layout="vertical">
                  <XAxis type="number" tickFormatter={(v) => formatCompactMoney(v)} stroke="#627d98" />
                  <YAxis type="category" dataKey="category" width={100} stroke="#627d98" />
                  <Tooltip
                    formatter={(value: number) => formatMoney(value)}
                    contentStyle={{
                      backgroundColor: '#1e3a5f',
                      border: '1px solid #334e68',
                      borderRadius: '8px',
                      color: '#e2e8f0'
                    }}
                  />
                  <Bar dataKey="value_kwd" fill="#fbbf24" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Currency */}
        {currExposure && currExposure.items.length > 0 && (
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-brand-100 mb-6">Currency Exposure</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={currExposure.items}
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    dataKey="value_kwd"
                    nameKey="category"
                    label={({ category, percentage }) => `${category}: ${percentage}%`}
                    labelLine={false}
                  >
                    {currExposure.items.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(value: number) => formatMoney(value)}
                    contentStyle={{
                      backgroundColor: '#1e3a5f',
                      border: '1px solid #334e68',
                      borderRadius: '8px',
                      color: '#e2e8f0'
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
