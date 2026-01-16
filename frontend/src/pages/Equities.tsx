import { useEffect, useState } from 'react';
import { Plus, Search, Filter, TrendingUp, TrendingDown, Pencil, Trash2 } from 'lucide-react';
import { getEquities, deleteEquity } from '../services/api';
import { EquityForm } from '../components/Forms';
import type { EquityHolding, PaginatedResponse } from '../types';
import { formatMoney, formatNumber, getGainLossColor, getStatusColor } from '../utils/format';
import clsx from 'clsx';

export default function Equities() {
  const [data, setData] = useState<PaginatedResponse<EquityHolding> | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [editItem, setEditItem] = useState<EquityHolding | null>(null);
  const [deleteItem, setDeleteItem] = useState<EquityHolding | null>(null);
  const [deleting, setDeleting] = useState(false);

  const fetchData = async () => {
    try {
      const response = await getEquities();
      setData(response);
    } catch (error) {
      console.error('Failed to fetch equities:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const filteredItems = data?.items.filter(item =>
    item.ticker.toLowerCase().includes(search.toLowerCase()) ||
    item.name.toLowerCase().includes(search.toLowerCase())
  ) || [];

  const handleDelete = async () => {
    if (!deleteItem) return;
    setDeleting(true);
    try {
      await deleteEquity(deleteItem.id);
      fetchData();
      setDeleteItem(null);
    } catch (error) {
      console.error('Failed to delete:', error);
    } finally {
      setDeleting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-pulse text-gold-400">Loading equities...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-display font-bold text-brand-50 mb-2">Public Equities</h1>
          <p className="text-brand-400">
            {data?.total || 0} holdings across global exchanges
          </p>
        </div>
        <button onClick={() => setShowAddForm(true)} className="btn-primary flex items-center gap-2">
          <Plus className="w-5 h-5" />
          Add Holding
        </button>
      </div>

      {(showAddForm || editItem) && (
        <EquityForm
          onClose={() => { setShowAddForm(false); setEditItem(null); }}
          onSuccess={() => {
            fetchData();
            setShowAddForm(false);
            setEditItem(null);
          }}
          initialData={editItem || undefined}
        />
      )}

      {deleteItem && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="card max-w-md w-full p-6">
            <h2 className="text-xl font-semibold text-brand-50 mb-4">Delete Holding</h2>
            <p className="text-brand-300 mb-6">
              Are you sure you want to delete <span className="text-gold-400 font-semibold">{deleteItem.ticker}</span>? This action cannot be undone.
            </p>
            <div className="flex gap-3">
              <button onClick={handleDelete} disabled={deleting} className="btn-primary flex-1 bg-rose-600 hover:bg-rose-500">
                {deleting ? 'Deleting...' : 'Delete'}
              </button>
              <button onClick={() => setDeleteItem(null)} className="btn-secondary flex-1">Cancel</button>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="card p-4 flex flex-wrap gap-4">
        <div className="flex-1 min-w-64 relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-brand-500" />
          <input
            type="text"
            placeholder="Search by ticker or name..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input w-full pl-12"
          />
        </div>
        <button className="btn-secondary flex items-center gap-2">
          <Filter className="w-5 h-5" />
          Filters
        </button>
      </div>

      {/* Table */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-brand-800">
                <th className="table-cell table-header text-left">Ticker</th>
                <th className="table-cell table-header text-left">Name</th>
                <th className="table-cell table-header text-left">Exchange</th>
                <th className="table-cell table-header text-right">Quantity</th>
                <th className="table-cell table-header text-right">Cost Basis</th>
                <th className="table-cell table-header text-right">Current Value</th>
                <th className="table-cell table-header text-right">Gain/Loss</th>
                <th className="table-cell table-header text-center">Status</th>
                <th className="table-cell table-header text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredItems.length === 0 ? (
                <tr>
                  <td colSpan={9} className="table-cell text-center text-brand-400 py-12">
                    {search ? 'No holdings match your search' : 'No equity holdings yet'}
                  </td>
                </tr>
              ) : (
                filteredItems.map((holding) => (
                  <tr key={holding.id} className="table-row cursor-pointer">
                    <td className="table-cell">
                      <span className="font-mono font-semibold text-gold-400">
                        {holding.ticker}
                      </span>
                    </td>
                    <td className="table-cell">
                      <div>
                        <p className="font-medium text-brand-100">{holding.name}</p>
                        {holding.sector && (
                          <p className="text-xs text-brand-500">{holding.sector}</p>
                        )}
                      </div>
                    </td>
                    <td className="table-cell">
                      <span className="badge badge-info">
                        {holding.exchange.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="table-cell text-right font-mono">
                      {formatNumber(holding.quantity)}
                    </td>
                    <td className="table-cell text-right font-mono">
                      {formatMoney(holding.cost_basis_amount, holding.cost_basis_currency)}
                    </td>
                    <td className="table-cell text-right font-mono">
                      {holding.current_value_kwd
                        ? formatMoney(holding.current_value_kwd)
                        : '-'
                      }
                    </td>
                    <td className="table-cell text-right">
                      <div className={clsx(
                        "flex items-center justify-end gap-1 font-mono",
                        getGainLossColor(holding.unrealized_gain_loss)
                      )}>
                        {holding.unrealized_gain_loss >= 0 ? (
                          <TrendingUp className="w-4 h-4" />
                        ) : (
                          <TrendingDown className="w-4 h-4" />
                        )}
                        {formatMoney(Math.abs(holding.unrealized_gain_loss))}
                      </div>
                    </td>
                    <td className="table-cell text-center">
                      <span className={clsx("badge", getStatusColor(holding.status))}>
                        {holding.status}
                      </span>
                    </td>
                    <td className="table-cell text-center">
                      <div className="flex items-center justify-center gap-2">
                        <button
                          onClick={(e) => { e.stopPropagation(); setEditItem(holding); }}
                          className="p-1.5 hover:bg-brand-700 rounded transition-colors"
                          title="Edit"
                        >
                          <Pencil className="w-4 h-4 text-brand-400" />
                        </button>
                        <button
                          onClick={(e) => { e.stopPropagation(); setDeleteItem(holding); }}
                          className="p-1.5 hover:bg-rose-500/20 rounded transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="w-4 h-4 text-rose-400" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
