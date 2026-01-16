import { useState } from 'react';
import { X } from 'lucide-react';
import { createProperty, updateProperty } from '../../services/api';
import type { Property } from '../../types';

interface PropertyFormProps {
  onClose: () => void;
  onSuccess: () => void;
  initialData?: Property;
}

export default function PropertyForm({ onClose, onSuccess, initialData }: PropertyFormProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    property_type: initialData?.property_type || 'commercial',
    address: initialData?.address || '',
    city: initialData?.city || 'Kuwait',
    country: initialData?.country || 'Kuwait',
    purchase_price_amount: initialData?.purchase_price_amount || 0,
    purchase_price_currency: initialData?.purchase_price_currency || 'KWD',
    purchase_date: initialData?.purchase_date || '',
    ownership_entity: initialData?.ownership_entity || '',
    ownership_percentage: initialData?.ownership_percentage || 10000,
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
        await updateProperty(initialData.id, formData);
      } else {
        await createProperty(formData);
      }
      onSuccess();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save property');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="card max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 flex items-center justify-between p-6 border-b border-brand-800">
          <h2 className="text-xl font-semibold text-brand-50">{initialData ? 'Edit Property' : 'Add Property'}</h2>
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
              <label className="label">Property Name</label>
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
              <label className="label">Type</label>
              <select name="property_type" value={formData.property_type} onChange={handleChange} className="input w-full">
                <option value="commercial">Commercial</option>
                <option value="residential">Residential</option>
                <option value="mixed">Mixed</option>
                <option value="land">Land</option>
              </select>
            </div>

            <div>
              <label className="label">Address</label>
              <input
                type="text"
                name="address"
                value={formData.address}
                onChange={handleChange}
                className="input w-full"
              />
            </div>

            <div>
              <label className="label">City</label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
                className="input w-full"
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

            <div className="col-span-2">
              <label className="label">Ownership Entity (SPV/Company)</label>
              <input
                type="text"
                name="ownership_entity"
                value={formData.ownership_entity}
                onChange={handleChange}
                className="input w-full"
              />
            </div>

            <div>
              <label className="label">Ownership % (basis points)</label>
              <input
                type="number"
                name="ownership_percentage"
                value={formData.ownership_percentage}
                onChange={handleChange}
                className="input w-full"
                placeholder="10000 = 100%"
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
