import { useState } from 'react';
import { X } from 'lucide-react';
import { createEquity, updateEquity } from '../../services/api';
import type { EquityHolding } from '../../types';

interface EquityFormProps {
  onClose: () => void;
  onSuccess: () => void;
  initialData?: EquityHolding;
}

export default function EquityForm({ onClose, onSuccess, initialData }: EquityFormProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    ticker: initialData?.ticker || '',
    name: initialData?.name || '',
    exchange: initialData?.exchange || 'NYSE',
    sector: initialData?.sector || '',
    country: initialData?.country || '',
    quantity: initialData?.quantity || 0,
    cost_basis_amount: initialData?.cost_basis_amount || 0,
    cost_basis_currency: initialData?.cost_basis_currency || 'KWD',
    notes: initialData?.notes || '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target as any;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseInt(value) : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (initialData?.id) {
        await updateEquity(initialData.id, formData);
      } else {
        await createEquity(formData);
      }
      onSuccess();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save equity');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="card max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 flex items-center justify-between p-6 border-b border-brand-800">
          <h2 className="text-xl font-semibold text-brand-50">
            {initialData ? 'Edit Equity' : 'Add Equity Holding'}
          </h2>
          <button onClick={onClose} className="p-1 hover:bg-brand-800 rounded">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="bg-rose-500/10 border border-rose-500/30 text-rose-400 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Ticker</label>
              <input
                type="text"
                name="ticker"
                value={formData.ticker}
                onChange={handleChange}
                className="input w-full"
                required
              />
            </div>
            <div>
              <label className="label">Company Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="input w-full"
                required
              />
            </div>

            <div>
              <label className="label">Exchange</label>
              <select name="exchange" value={formData.exchange} onChange={handleChange} className="input w-full">
                <option value="NYSE">NYSE</option>
                <option value="NASDAQ">NASDAQ</option>
                <option value="LSE">LSE</option>
                <option value="BOURSA_KUWAIT">Boursa Kuwait</option>
                <option value="TADAWUL">Tadawul</option>
                <option value="DFM">DFM</option>
              </select>
            </div>

            <div>
              <label className="label">Sector</label>
              <input
                type="text"
                name="sector"
                value={formData.sector}
                onChange={handleChange}
                className="input w-full"
              />
            </div>

            <div>
              <label className="label">Country</label>
              <input
                type="text"
                name="country"
                value={formData.country}
                onChange={handleChange}
                className="input w-full"
              />
            </div>

            <div>
              <label className="label">Quantity</label>
              <input
                type="number"
                name="quantity"
                value={formData.quantity}
                onChange={handleChange}
                className="input w-full"
                required
              />
            </div>

            <div>
              <label className="label">Cost Basis Amount</label>
              <input
                type="number"
                name="cost_basis_amount"
                value={formData.cost_basis_amount}
                onChange={handleChange}
                className="input w-full"
                required
              />
            </div>

            <div>
              <label className="label">Currency</label>
              <select name="cost_basis_currency" value={formData.cost_basis_currency} onChange={handleChange} className="input w-full">
                <option value="KWD">KWD</option>
                <option value="USD">USD</option>
                <option value="EUR">EUR</option>
                <option value="GBP">GBP</option>
              </select>
            </div>
          </div>

          <div>
            <label className="label">Notes</label>
            <textarea
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              className="input w-full h-20 resize-none"
            />
          </div>

          <div className="flex gap-3 pt-4">
            <button type="submit" disabled={loading} className="btn-primary flex-1">
              {loading ? 'Saving...' : 'Save'}
            </button>
            <button type="button" onClick={onClose} className="btn-secondary flex-1">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
