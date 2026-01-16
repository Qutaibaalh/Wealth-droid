import { useEffect, useState } from 'react';
import { Plus, Search, Wallet, ArrowDownRight, ArrowUpRight, Pencil, Trash2 } from 'lucide-react';
import { getPrivateFunds, deletePrivateFund } from '../services/api';
import { PrivateFundForm } from '../components/Forms';
import type { PrivateFund, PaginatedResponse } from '../types';
import { formatMoney, formatBps, getStatusColor } from '../utils/format';
import clsx from 'clsx';

export default function PrivateFunds() {
  const [data, setData] = useState<PaginatedResponse<PrivateFund> | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [editItem, setEditItem] = useState<PrivateFund | null>(null);
  const [deleteItem, setDeleteItem] = useState<PrivateFund | null>(null);
  const [deleting, setDeleting] = useState(false);

  const fetchData = async () => {
    try {
      const response = await getPrivateFunds();
      setData(response);
    } catch (error) {
      console.error('Failed to fetch private funds:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const filteredItems = data?.items.filter(item =>
    item.name.toLowerCase().includes(search.toLowerCase()) ||
    (item.fund_manager && item.fund_manager.toLowerCase().includes(search.toLowerCase()))
  ) || [];

  const handleDelete = async () => {
    if (!deleteItem) return;
    setDeleting(true);
    try {
      await deletePrivateFund(deleteItem.id);
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
        <div className="animate-pulse text-gold-400">Loading private funds...</div>
      </div>
    );
  }

  const totalCommitted = data?.items.reduce((sum, f) => sum + f.committed_capital_amount, 0) || 0;
  const totalCalled = data?.items.reduce((sum, f) => sum + f.called_capital_amount, 0) || 0;
  const totalDistributed = data?.items.reduce((sum, f) => sum + f.distributions_received, 0) || 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-display font-bold text-brand-50 mb-2">Private Funds & PE</h1>
          <p className="text-brand-400">
            {data?.total || 0} fund investments and co-investments
          </p>
        </div>
        <button onClick={() => setShowAddForm(true)} className="btn-primary flex items-center gap-2">
          <Plus className="w-5 h-5" />
          Add Fund
        </button>
      </div>

      {(showAddForm || editItem) && (
        <PrivateFundForm
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
            <h2 className="text-xl font-semibold text-brand-50 mb-4">Delete Fund</h2>
            <p className="text-brand-300 mb-6">
              Are you sure you want to delete <span className="text-gold-400 font-semibold">{deleteItem.name}</span>? This action cannot be undone.
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

      {/* Summary cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-800/50 rounded-lg">
              <Wallet className="w-5 h-5 text-brand-400" />
            </div>
            <span className="text-sm text-brand-400">Total Committed</span>
          </div>
          <p className="stat-value text-2xl">{formatMoney(totalCommitted, 'USD')}</p>
        </div>
        <div className="card p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-800/50 rounded-lg">
              <ArrowUpRight className="w-5 h-5 text-amber-400" />
            </div>
            <span className="text-sm text-brand-400">Total Called</span>
          </div>
          <p className="stat-value text-2xl">{formatMoney(totalCalled, 'USD')}</p>
        </div>
        <div className="card p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-800/50 rounded-lg">
              <ArrowDownRight className="w-5 h-5 text-emerald-400" />
            </div>
            <span className="text-sm text-brand-400">Total Distributed</span>
          </div>
          <p className="stat-value text-2xl">{formatMoney(totalDistributed, 'USD')}</p>
        </div>
      </div>

      {/* Search */}
      <div className="card p-4">
        <div className="relative max-w-md">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-brand-500" />
          <input
            type="text"
            placeholder="Search by fund name or manager..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input w-full pl-12"
          />
        </div>
      </div>

      {/* Table */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-brand-800">
                <th className="table-cell table-header text-left">Fund Name</th>
                <th className="table-cell table-header text-left">Type</th>
                <th className="table-cell table-header text-left">Manager</th>
                <th className="table-cell table-header text-right">Committed</th>
                <th className="table-cell table-header text-right">Called</th>
                <th className="table-cell table-header text-right">NAV</th>
                <th className="table-cell table-header text-center">IRR</th>
                <th className="table-cell table-header text-center">TVPI</th>
                <th className="table-cell table-header text-center">Status</th>
                <th className="table-cell table-header text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredItems.length === 0 ? (
                <tr>
                  <td colSpan={10} className="table-cell text-center text-brand-400 py-12">
                    {search ? 'No funds match your search' : 'No private fund investments yet'}
                  </td>
                </tr>
              ) : (
                filteredItems.map((fund) => (
                  <tr key={fund.id} className="table-row cursor-pointer">
                    <td className="table-cell">
                      <div>
                        <p className="font-medium text-brand-100">{fund.name}</p>
                        {fund.vintage_year && (
                          <p className="text-xs text-brand-500">Vintage {fund.vintage_year}</p>
                        )}
                      </div>
                    </td>
                    <td className="table-cell">
                      <span className="badge badge-info capitalize">
                        {fund.fund_type.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="table-cell text-brand-300">
                      {fund.fund_manager || '-'}
                    </td>
                    <td className="table-cell text-right font-mono">
                      {formatMoney(fund.committed_capital_amount, fund.committed_capital_currency)}
                    </td>
                    <td className="table-cell text-right font-mono">
                      {formatMoney(fund.called_capital_amount, fund.committed_capital_currency)}
                    </td>
                    <td className="table-cell text-right font-mono">
                      {fund.current_nav_kwd
                        ? formatMoney(fund.current_nav_kwd)
                        : '-'
                      }
                    </td>
                    <td className="table-cell text-center">
                      {fund.irr_bps ? (
                        <span className={clsx(
                          "font-mono font-semibold",
                          fund.irr_bps >= 0 ? "text-emerald-400" : "text-rose-400"
                        )}>
                          {formatBps(fund.irr_bps)}
                        </span>
                      ) : '-'}
                    </td>
                    <td className="table-cell text-center">
                      {fund.tvpi_bps ? (
                        <span className="font-mono">
                          {(fund.tvpi_bps / 10000).toFixed(2)}x
                        </span>
                      ) : '-'}
                    </td>
                    <td className="table-cell text-center">
                      <span className={clsx("badge", getStatusColor(fund.status))}>
                        {fund.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="table-cell text-center">
                      <div className="flex items-center justify-center gap-2">
                        <button
                          onClick={(e) => { e.stopPropagation(); setEditItem(fund); }}
                          className="p-1.5 hover:bg-brand-700 rounded transition-colors"
                          title="Edit"
                        >
                          <Pencil className="w-4 h-4 text-brand-400" />
                        </button>
                        <button
                          onClick={(e) => { e.stopPropagation(); setDeleteItem(fund); }}
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
