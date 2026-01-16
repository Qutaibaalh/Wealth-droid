import { useState } from 'react';
import { X } from 'lucide-react';
import { createPrivateFund, updatePrivateFund } from '../../services/api';
import type { PrivateFund } from '../../types';

interface PrivateFundFormProps {
  onClose: () => void;
  onSuccess: () => void;
  initialData?: PrivateFund;
}

export default function PrivateFundForm({ onClose, onSuccess, initialData }: PrivateFundFormProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    fund_type: initialData?.fund_type || 'private_equity',
    fund_manager: initialData?.fund_manager || '',
    vintage_year: initialData?.vintage_year || new Date().getFullYear(),
    geography: initialData?.geography || 'MENA',
    sector: initialData?.sector || '',
    committed_capital_amount: initialData?.committed_capital_amount || 0,
    committed_capital_currency: initialData?.committed_capital_currency || 'USD',
    management_fee_bps: initialData?.management_fee_bps || 200,
    carried_interest_bps: initialData?.carried_interest_bps || 2000,
    fund_term_years: initialData?.fund_term_years || 10,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
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
        await updatePrivateFund(initialData.id, formData);
      } else {
        await createPrivateFund(formData);
      }
      onSuccess();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save private fund');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="card max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 flex items-center justify-between p-6 border-b border-brand-800">
          <h2 className="text-xl font-semibold text-brand-50">{initialData ? 'Edit Private Fund' : 'Add Private Fund'}</h2>
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
              <label className="label">Fund Name</label>
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
              <label className="label">Fund Type</label>
              <select name="fund_type" value={formData.fund_type} onChange={handleChange} className="input w-full">
                <option value="private_equity">Private Equity</option>
                <option value="venture_capital">Venture Capital</option>
                <option value="hedge_fund">Hedge Fund</option>
                <option value="real_estate_fund">Real Estate Fund</option>
                <option value="infrastructure">Infrastructure</option>
              </select>
            </div>

            <div>
              <label className="label">Fund Manager</label>
              <input
                type="text"
                name="fund_manager"
                value={formData.fund_manager}
                onChange={handleChange}
                className="input w-full"
              />
            </div>

            <div>
              <label className="label">Vintage Year</label>
              <input
                type="number"
                name="vintage_year"
                value={formData.vintage_year}
                onChange={handleChange}
                className="input w-full"
              />
            </div>

            <div>
              <label className="label">Geography</label>
              <input
                type="text"
                name="geography"
                value={formData.geography}
                onChange={handleChange}
                className="input w-full"
              />
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
              <label className="label">Committed Capital</label>
              <input
                type="number"
                name="committed_capital_amount"
                value={formData.committed_capital_amount}
                onChange={handleChange}
                className="input w-full"
                required
              />
            </div>

            <div>
              <label className="label">Management Fee (bps)</label>
              <input
                type="number"
                name="management_fee_bps"
                value={formData.management_fee_bps}
                onChange={handleChange}
                className="input w-full"
                placeholder="200 = 2%"
              />
            </div>

            <div>
              <label className="label">Carried Interest (bps)</label>
              <input
                type="number"
                name="carried_interest_bps"
                value={formData.carried_interest_bps}
                onChange={handleChange}
                className="input w-full"
                placeholder="2000 = 20%"
              />
            </div>

            <div>
              <label className="label">Fund Term (years)</label>
              <input
                type="number"
                name="fund_term_years"
                value={formData.fund_term_years}
                onChange={handleChange}
                className="input w-full"
              />
            </div>
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
