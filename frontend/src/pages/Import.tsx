import { useState, useCallback } from 'react';
import { Upload, FileSpreadsheet, Download, AlertCircle, CheckCircle2, X } from 'lucide-react';
import clsx from 'clsx';
import api from '../services/api';

type AssetClass = 'equities' | 'fixed-income' | 'real-estate' | 'private-funds';

interface ImportResult {
  success: boolean;
  created: number;
  errors: { row: number; message: string }[];
}

const assetClassConfig: Record<AssetClass, { label: string; endpoint: string; templateFields: string[] }> = {
  'equities': {
    label: 'Equities',
    endpoint: '/import/equities',
    templateFields: ['ticker', 'name', 'exchange', 'sector', 'country', 'quantity', 'cost_basis_amount', 'cost_basis_currency', 'purchase_date']
  },
  'fixed-income': {
    label: 'Fixed Income',
    endpoint: '/import/fixed-income',
    templateFields: ['name', 'isin', 'instrument_type', 'issuer', 'face_value_amount', 'face_value_currency', 'purchase_price_amount', 'purchase_date', 'coupon_rate', 'maturity_date']
  },
  'real-estate': {
    label: 'Real Estate',
    endpoint: '/import/real-estate',
    templateFields: ['name', 'property_type', 'address', 'city', 'country', 'purchase_price_amount', 'purchase_price_currency', 'purchase_date', 'ownership_entity', 'ownership_percentage']
  },
  'private-funds': {
    label: 'Private Funds',
    endpoint: '/import/private-funds',
    templateFields: ['name', 'fund_type', 'fund_manager', 'vintage_year', 'geography', 'sector', 'committed_capital_amount', 'committed_capital_currency']
  }
};

export default function Import() {
  const [selectedAssetClass, setSelectedAssetClass] = useState<AssetClass>('equities');
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<Record<string, string>[] | null>(null);
  const [importing, setImporting] = useState(false);
  const [result, setResult] = useState<ImportResult | null>(null);
  const [dragOver, setDragOver] = useState(false);

  const handleFileSelect = useCallback((selectedFile: File) => {
    if (!selectedFile.name.match(/\.(xlsx|xls|csv)$/i)) {
      alert('Please select an Excel or CSV file');
      return;
    }
    setFile(selectedFile);
    setResult(null);
    parseFile(selectedFile);
  }, []);

  const parseFile = async (file: File) => {
    const text = await file.text();
    const lines = text.split('\n').filter(line => line.trim());
    if (lines.length < 2) {
      alert('File appears to be empty');
      return;
    }
    
    const headers = lines[0].split(',').map(h => h.trim().toLowerCase().replace(/"/g, ''));
    const rows = lines.slice(1, 6).map(line => {
      const values = line.split(',').map(v => v.trim().replace(/"/g, ''));
      const row: Record<string, string> = {};
      headers.forEach((h, i) => {
        row[h] = values[i] || '';
      });
      return row;
    });
    
    setPreview(rows);
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      handleFileSelect(droppedFile);
    }
  }, [handleFileSelect]);

  const handleImport = async () => {
    if (!file) return;
    setImporting(true);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post<ImportResult>(
        assetClassConfig[selectedAssetClass].endpoint,
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setResult(response.data);
    } catch (error: any) {
      setResult({
        success: false,
        created: 0,
        errors: [{ row: 0, message: error.response?.data?.detail || 'Import failed' }]
      });
    } finally {
      setImporting(false);
    }
  };

  const downloadTemplate = (assetClass: AssetClass) => {
    const config = assetClassConfig[assetClass];
    const csvContent = config.templateFields.join(',') + '\n';
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${assetClass}_template.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const clearFile = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-display font-bold text-brand-50 mb-2">Import Data</h1>
        <p className="text-brand-400">Bulk import holdings from Excel or CSV files</p>
      </div>

      {/* Asset class selection */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-brand-100 mb-4">Select Asset Class</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {(Object.keys(assetClassConfig) as AssetClass[]).map((key) => (
            <button
              key={key}
              onClick={() => { setSelectedAssetClass(key); clearFile(); }}
              className={clsx(
                "p-4 rounded-lg border-2 transition-all text-left",
                selectedAssetClass === key
                  ? "border-gold-500 bg-gold-500/10"
                  : "border-brand-700 hover:border-brand-600 bg-brand-800/50"
              )}
            >
              <FileSpreadsheet className={clsx(
                "w-6 h-6 mb-2",
                selectedAssetClass === key ? "text-gold-400" : "text-brand-400"
              )} />
              <span className={clsx(
                "font-medium",
                selectedAssetClass === key ? "text-gold-400" : "text-brand-200"
              )}>
                {assetClassConfig[key].label}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Template download */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-brand-100 mb-4">Download Template</h2>
        <p className="text-brand-400 text-sm mb-4">
          Download the CSV template with required columns for {assetClassConfig[selectedAssetClass].label.toLowerCase()}.
        </p>
        <button
          onClick={() => downloadTemplate(selectedAssetClass)}
          className="btn-secondary flex items-center gap-2"
        >
          <Download className="w-4 h-4" />
          Download {assetClassConfig[selectedAssetClass].label} Template
        </button>
        <div className="mt-4 text-xs text-brand-500">
          <span className="font-medium">Required columns:</span>{' '}
          {assetClassConfig[selectedAssetClass].templateFields.join(', ')}
        </div>
      </div>

      {/* File upload */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-brand-100 mb-4">Upload File</h2>
        
        {!file ? (
          <div
            onDrop={handleDrop}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            className={clsx(
              "border-2 border-dashed rounded-xl p-12 text-center transition-colors",
              dragOver ? "border-gold-500 bg-gold-500/5" : "border-brand-700 hover:border-brand-600"
            )}
          >
            <Upload className="w-12 h-12 mx-auto mb-4 text-brand-500" />
            <p className="text-brand-300 mb-2">Drag and drop your file here, or</p>
            <label className="btn-primary inline-flex cursor-pointer">
              Browse Files
              <input
                type="file"
                accept=".xlsx,.xls,.csv"
                onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
                className="hidden"
              />
            </label>
            <p className="text-brand-500 text-sm mt-4">Supports .xlsx, .xls, and .csv files</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-brand-800/50 rounded-lg">
              <div className="flex items-center gap-3">
                <FileSpreadsheet className="w-8 h-8 text-gold-400" />
                <div>
                  <p className="font-medium text-brand-100">{file.name}</p>
                  <p className="text-sm text-brand-500">{(file.size / 1024).toFixed(1)} KB</p>
                </div>
              </div>
              <button onClick={clearFile} className="p-2 hover:bg-brand-700 rounded">
                <X className="w-5 h-5 text-brand-400" />
              </button>
            </div>

            {/* Preview table */}
            {preview && preview.length > 0 && (
              <div>
                <h3 className="text-sm font-medium text-brand-300 mb-2">Preview (first 5 rows)</h3>
                <div className="overflow-x-auto rounded-lg border border-brand-700">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-brand-800">
                        {Object.keys(preview[0]).map((key) => (
                          <th key={key} className="px-3 py-2 text-left text-brand-400 font-medium">
                            {key}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {preview.map((row, i) => (
                        <tr key={i} className="border-t border-brand-700">
                          {Object.values(row).map((val, j) => (
                            <td key={j} className="px-3 py-2 text-brand-200">
                              {val || '-'}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            <button
              onClick={handleImport}
              disabled={importing}
              className="btn-primary w-full"
            >
              {importing ? 'Importing...' : `Import to ${assetClassConfig[selectedAssetClass].label}`}
            </button>
          </div>
        )}
      </div>

      {/* Result */}
      {result && (
        <div className={clsx(
          "card p-6",
          result.success ? "border-emerald-500/30" : "border-rose-500/30"
        )}>
          <div className="flex items-start gap-3">
            {result.success ? (
              <CheckCircle2 className="w-6 h-6 text-emerald-400 flex-shrink-0" />
            ) : (
              <AlertCircle className="w-6 h-6 text-rose-400 flex-shrink-0" />
            )}
            <div className="flex-1">
              <h3 className={clsx(
                "font-semibold mb-2",
                result.success ? "text-emerald-400" : "text-rose-400"
              )}>
                {result.success ? 'Import Successful' : 'Import Failed'}
              </h3>
              {result.created > 0 && (
                <p className="text-brand-300 mb-2">
                  Successfully imported {result.created} record{result.created !== 1 ? 's' : ''}.
                </p>
              )}
              {result.errors.length > 0 && (
                <div className="mt-3">
                  <p className="text-sm text-brand-400 mb-2">Errors:</p>
                  <ul className="space-y-1">
                    {result.errors.map((err, i) => (
                      <li key={i} className="text-sm text-rose-400">
                        {err.row > 0 ? `Row ${err.row}: ` : ''}{err.message}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
