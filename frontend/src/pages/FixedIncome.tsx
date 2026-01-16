import { useEffect, useState } from 'react';
import { Plus, Search, Calendar, Percent, Pencil, Trash2 } from 'lucide-react';
import { getFixedIncome, deleteFixedIncome } from '../services/api';
import { FixedIncomeForm } from '../components/Forms';
import type { FixedIncomeHolding, PaginatedResponse } from '../types';
import { formatMoney, formatDate, formatBps, getStatusColor } from '../utils/format';
import clsx from 'clsx';

export default function FixedIncome() {
  const [data, setData] = useState<PaginatedResponse<FixedIncomeHolding> | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [editItem, setEditItem] = useState<FixedIncomeHolding | null>(null);
  const [deleteItem, setDeleteItem] = useState<FixedIncomeHolding | null>(null);
  const [deleting, setDeleting] = useState(false);

  const fetchData = async () => {
    try {
      const response = await getFixedIncome();
      setData(response);
    } catch (error) {
      console.error('Failed to fetch fixed income:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const filteredItems = data?.items.filter(item =>
    item.name.toLowerCase().includes(search.toLowerCase()) ||
    (item.isin && item.isin.toLowerCase().includes(search.toLowerCase()))
  ) || [];

  const handleDelete = async () => {
    if (!deleteItem) return;
    setDeleting(true);
    try {
      await deleteFixedIncome(deleteItem.id);
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
        <div className="animate-pulse text-gold-400">Loading fixed income...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-display font-bold text-brand-50 mb-2">Fixed Income</h1>
          <p className="text-brand-400">
            {data?.total || 0} bonds, sukuk, and fixed income funds
          </p>
        </div>
        <button onClick={() => setShowAddForm(true)} className="btn-primary flex items-center gap-2">
          <Plus className="w-5 h-5" />
          Add Holding
        </button>
      </div>

      {(showAddForm || editItem) && (
        <FixedIncomeForm
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

      {/* Search */}
      <div className="card p-4">
        <div className="relative max-w-md">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-brand-500" />
          <input
            type="text"
            placeholder="Search by name or ISIN..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input w-full pl-12"
          />
        </div>
      </div>

      {/* Grid of cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredItems.length === 0 ? (
          <div className="col-span-full text-center text-brand-400 py-12 card">
            {search ? 'No holdings match your search' : 'No fixed income holdings yet'}
          </div>
        ) : (
          filteredItems.map((holding) => (
            <div key={holding.id} className="card card-hover p-6 cursor-pointer relative group">
              <div className="absolute top-4 right-4 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
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
              <div className="flex items-start justify-between mb-4">
                <div>
                  <span className={clsx("badge mb-2", getStatusColor(holding.status))}>
                    {holding.instrument_type.replace('_', ' ')}
                  </span>
                  <h3 className="font-semibold text-brand-100 line-clamp-2">{holding.name}</h3>
                  {holding.issuer && (
                    <p className="text-sm text-brand-400 mt-1">{holding.issuer}</p>
                  )}
                </div>
              </div>

              <div className="space-y-3 mt-4">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-brand-400">Face Value</span>
                  <span className="font-mono text-brand-100">
                    {formatMoney(holding.face_value_amount, holding.face_value_currency)}
                  </span>
                </div>
                
                {holding.coupon_rate && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-brand-400 flex items-center gap-1">
                      <Percent className="w-4 h-4" />
                      Coupon Rate
                    </span>
                    <span className="font-mono text-gold-400">
                      {formatBps(holding.coupon_rate)}
                    </span>
                  </div>
                )}
                
                {holding.maturity_date && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-brand-400 flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      Maturity
                    </span>
                    <span className="text-brand-100">
                      {formatDate(holding.maturity_date)}
                    </span>
                  </div>
                )}

                {holding.current_value_kwd && (
                  <div className="flex items-center justify-between text-sm pt-3 border-t border-brand-800/50">
                    <span className="text-brand-400">Current Value</span>
                    <span className="font-mono font-semibold text-brand-100">
                      {formatMoney(holding.current_value_kwd)}
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
