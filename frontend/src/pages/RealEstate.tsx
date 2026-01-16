import { useEffect, useState } from 'react';
import { Plus, Building2, MapPin, Pencil, Trash2 } from 'lucide-react';
import { getProperties, getOccupancyReport, deleteProperty } from '../services/api';
import { PropertyForm } from '../components/Forms';
import type { Property, OccupancyReport, PaginatedResponse } from '../types';
import { formatMoney } from '../utils/format';
import clsx from 'clsx';

export default function RealEstate() {
  const [properties, setProperties] = useState<PaginatedResponse<Property> | null>(null);
  const [occupancy, setOccupancy] = useState<OccupancyReport[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [view, setView] = useState<'properties' | 'occupancy'>('properties');
  const [showAddForm, setShowAddForm] = useState(false);
  const [editItem, setEditItem] = useState<Property | null>(null);
  const [deleteItem, setDeleteItem] = useState<Property | null>(null);
  const [deleting, setDeleting] = useState(false);

  const fetchData = async () => {
    try {
      const [propertiesData, occupancyData] = await Promise.all([
        getProperties(),
        getOccupancyReport()
      ]);
      setProperties(propertiesData);
      setOccupancy(occupancyData);
    } catch (error) {
      console.error('Failed to fetch real estate data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleDelete = async () => {
    if (!deleteItem) return;
    setDeleting(true);
    try {
      await deleteProperty(deleteItem.id);
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
        <div className="animate-pulse text-gold-400">Loading real estate...</div>
      </div>
    );
  }

  const totalUnits = properties?.items.reduce((sum, p) => sum + (p.units?.length || 0), 0) || 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-display font-bold text-brand-50 mb-2">Real Estate</h1>
          <p className="text-brand-400">
            {properties?.total || 0} properties with {totalUnits} total units
          </p>
        </div>
        <button onClick={() => setShowAddForm(true)} className="btn-primary flex items-center gap-2">
          <Plus className="w-5 h-5" />
          Add Property
        </button>
      </div>

      {(showAddForm || editItem) && (
        <PropertyForm
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
            <h2 className="text-xl font-semibold text-brand-50 mb-4">Delete Property</h2>
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

      {/* View toggle */}
      <div className="card p-1 inline-flex">
        <button
          onClick={() => setView('properties')}
          className={clsx(
            "px-4 py-2 rounded-lg text-sm font-medium transition-colors",
            view === 'properties'
              ? "bg-gold-500 text-brand-950"
              : "text-brand-400 hover:text-brand-100"
          )}
        >
          Properties
        </button>
        <button
          onClick={() => setView('occupancy')}
          className={clsx(
            "px-4 py-2 rounded-lg text-sm font-medium transition-colors",
            view === 'occupancy'
              ? "bg-gold-500 text-brand-950"
              : "text-brand-400 hover:text-brand-100"
          )}
        >
          Occupancy Report
        </button>
      </div>

      {view === 'properties' ? (
        /* Properties grid */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {!properties?.items.length ? (
            <div className="col-span-full text-center text-brand-400 py-12 card">
              No properties yet
            </div>
          ) : (
            properties.items.map((property) => (
              <div key={property.id} className="card card-hover overflow-hidden cursor-pointer relative group">
                <div className="absolute top-2 right-2 z-10 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    onClick={(e) => { e.stopPropagation(); setEditItem(property); }}
                    className="p-1.5 bg-brand-800/80 hover:bg-brand-700 rounded transition-colors"
                    title="Edit"
                  >
                    <Pencil className="w-4 h-4 text-brand-300" />
                  </button>
                  <button
                    onClick={(e) => { e.stopPropagation(); setDeleteItem(property); }}
                    className="p-1.5 bg-brand-800/80 hover:bg-rose-500/50 rounded transition-colors"
                    title="Delete"
                  >
                    <Trash2 className="w-4 h-4 text-rose-400" />
                  </button>
                </div>
                <div className="h-32 bg-gradient-to-br from-brand-800 to-brand-900 flex items-center justify-center">
                  <Building2 className="w-12 h-12 text-brand-600" />
                </div>
                <div className="p-6">
                  <div className="flex items-start justify-between mb-2">
                    <span className="badge badge-info capitalize">
                      {property.property_type}
                    </span>
                    <span className="text-xs text-brand-500">
                      {property.ownership_percentage / 100}% owned
                    </span>
                  </div>
                  <h3 className="font-semibold text-brand-100 text-lg mb-1">{property.name}</h3>
                  {(property.city || property.country) && (
                    <p className="text-sm text-brand-400 flex items-center gap-1 mb-4">
                      <MapPin className="w-4 h-4" />
                      {[property.city, property.country].filter(Boolean).join(', ')}
                    </p>
                  )}

                  <div className="grid grid-cols-2 gap-4 pt-4 border-t border-brand-800/50">
                    <div>
                      <p className="text-xs text-brand-500 uppercase">Purchase</p>
                      <p className="font-mono text-sm text-brand-100">
                        {formatMoney(property.purchase_price_amount, property.purchase_price_currency)}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-brand-500 uppercase">Current</p>
                      <p className="font-mono text-sm text-brand-100">
                        {property.current_value_amount
                          ? formatMoney(property.current_value_amount, property.current_value_currency || 'KWD')
                          : '-'
                        }
                      </p>
                    </div>
                  </div>

                  {property.ownership_entity && (
                    <p className="text-xs text-brand-500 mt-4">
                      via {property.ownership_entity}
                    </p>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      ) : (
        /* Occupancy report table */
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-brand-800">
                  <th className="table-cell table-header text-left">Property</th>
                  <th className="table-cell table-header text-center">Total Units</th>
                  <th className="table-cell table-header text-center">Occupied</th>
                  <th className="table-cell table-header text-center">Vacant</th>
                  <th className="table-cell table-header text-center">Occupancy Rate</th>
                  <th className="table-cell table-header text-right">Monthly Rent</th>
                  <th className="table-cell table-header text-right">Outstanding</th>
                </tr>
              </thead>
              <tbody>
                {occupancy.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="table-cell text-center text-brand-400 py-12">
                      No occupancy data available
                    </td>
                  </tr>
                ) : (
                  occupancy.map((report) => (
                    <tr key={report.property_id} className="table-row">
                      <td className="table-cell font-medium text-brand-100">
                        {report.property_name}
                      </td>
                      <td className="table-cell text-center font-mono">
                        {report.total_units}
                      </td>
                      <td className="table-cell text-center">
                        <span className="badge badge-success">{report.occupied_units}</span>
                      </td>
                      <td className="table-cell text-center">
                        <span className="badge badge-warning">{report.vacant_units}</span>
                      </td>
                      <td className="table-cell text-center">
                        <div className="flex items-center justify-center gap-2">
                          <div className="w-16 h-2 bg-brand-800 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-emerald-500 rounded-full"
                              style={{ width: `${report.occupancy_rate}%` }}
                            />
                          </div>
                          <span className="font-mono text-sm">{report.occupancy_rate}%</span>
                        </div>
                      </td>
                      <td className="table-cell text-right font-mono">
                        {formatMoney(report.total_monthly_rent, report.currency)}
                      </td>
                      <td className="table-cell text-right">
                        <span className={clsx(
                          "font-mono",
                          report.total_outstanding > 0 ? "text-rose-400" : "text-brand-400"
                        )}>
                          {formatMoney(report.total_outstanding, report.currency)}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
