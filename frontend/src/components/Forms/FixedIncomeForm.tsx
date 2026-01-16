import { useState } from 'react';
import { X } from 'lucide-react';
import { createFixedIncome, updateFixedIncome } from '../../services/api';
import type { FixedIncomeHolding } from '../../types';

interface FixedIncomeFormProps {
  onClose: () => void;
  onSuccess: () => void;
  initialData?: FixedIncomeHolding;
}

export default function FixedIncomeForm({ onClose, onSuccess, initialData }: FixedIncomeFormProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    isin: initialData?.isin || '',
    instrument_type: initialData?.instrument_type || 'corporate_bond',
    issuer: initialData?.issuer || '',
    face_value_amount: initialData?.face_value_amount || 0,
    face_value_currency: initialData?.face_value_currency || 'USD',
    purchase_price_amount: initialData?.purchase_price_amount || 0,
    purchase_price_currency: initialData?.purchase_price_currency || 'USD',
    purchase_date: initialData?.purchase_date || '',
    coupon_rate: initialData?.coupon_rate || 0,
    coupon_frequency: initialData?.coupon_frequency || 'annual',
    maturity_date: initialData?.maturity_date || '',
    expected_return_bps: initialData?.expected_return_bps || 0,
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
        await updateFixedIncome(initialData.id, formData);
      } else {
        await createFixedIncome(formData);
      }
      onSuccess();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save fixed income');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="card max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 flex items-center justify-between p-6 border-b border-brand-800">
          <h2 className="text-xl font-semibold text-brand-50">
            {initialData ? 'Edit Fixed Income' : 'Add Fixed Income Holding'}
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
              <label className="label">Name</label>
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
              <label className="label">ISIN</label>
              <input
                type="text"
                name="isin"
                value={formData.isin}
                onChange={handleChange}
                className="input w-full"
              />
            </div>

            <div>
              <label className="label">Type</label>
              <select name="instrument_type" value={formData.instrument_type} onChange={handleChange} className="input w-full">
                <option value="corporate_bond">Corporate Bond</option>
                <option value="government_bond">Government Bond</option>
                <option value="sukuk">Sukuk</option>
                <option value="fixed_income_fund">Fixed Income Fund</option>
              </select>
            </div>

            <div>
              <label className="label">Issuer</label>
              <input
                type="text"
                name="issuer"
                value={formData.issuer}
                onChange={handleChange}
                className="input w-full"
              />
            </div>

            <div>
              <label className="label">Face Value</label>
              <input
                type="number"
                name="face_value_amount"
                value={formData.face_value_amount}
                onChange={handleChange}
                className="input w-full"
                required
              />
            </div>

            <div>
              <label className="label">Purchase Price</label>
              <input
                type="number"
                name="purchase_price_amount"
                value={formData.purchase_price_amount}
                onChange={handleChange}
                className="input w-full"
                required
              />
            </div>

            <div>
              <label className="label">Purchase Date</label>
              <input
                type="date"
                name="purchase_date"
                value={formData.purchase_date}
                onChange={handleChange}
                className="input w-full"
                required
              />
            </div>

            <div>
              <label className="label">Maturity Date</label>
              <input
                type="date"
                name="maturity_date"
                value={formData.maturity_date}
                onChange={handleChange}
                className="input w-full"
              />
            </div>

            <div>
              <label className="label">Coupon Rate (%)</label>
              <input
                type="number"
                step="0.01"
                name="coupon_rate"
                value={formData.coupon_rate}
                onChange={handleChange}
                className="input w-full"
              />
            </div>

            <div>
              <label className="label">Coupon Frequency</label>
              <select name="coupon_frequency" value={formData.coupon_frequency} onChange={handleChange} className="input w-full">
                <option value="annual">Annual</option>
                <option value="semi-annual">Semi-Annual</option>
                <option value="quarterly">Quarterly</option>
              </select>
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
