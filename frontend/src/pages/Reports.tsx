import { useState } from 'react';
import { FileText, Download, PieChart, Building2, TrendingUp, Briefcase } from 'lucide-react';
import { downloadReport } from '../services/api';
import clsx from 'clsx';

const reportTypes = [
  {
    id: 'summary',
    name: 'Portfolio Summary',
    description: 'Complete overview of all asset classes with allocation breakdown',
    icon: PieChart,
    color: 'text-blue-400 bg-blue-500/10',
  },
  {
    id: 'equities',
    name: 'Equities Report',
    description: 'Detailed holdings, transactions, and performance for public equities',
    icon: TrendingUp,
    color: 'text-emerald-400 bg-emerald-500/10',
  },
  {
    id: 'real-estate',
    name: 'Real Estate Report',
    description: 'Properties, units, valuations, and occupancy analysis',
    icon: Building2,
    color: 'text-amber-400 bg-amber-500/10',
  },
  {
    id: 'private-funds',
    name: 'Private Funds Report',
    description: 'Fund investments, capital calls, distributions, and IRR analysis',
    icon: Briefcase,
    color: 'text-purple-400 bg-purple-500/10',
  },
];

export default function Reports() {
  const [downloading, setDownloading] = useState<string | null>(null);

  const handleDownload = async (reportType: string) => {
    setDownloading(reportType);
    try {
      await downloadReport(reportType);
    } catch (error) {
      console.error('Failed to download report:', error);
    } finally {
      setDownloading(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-display font-bold text-brand-50 mb-2">Reports</h1>
        <p className="text-brand-400">
          Generate and download PDF reports for review and distribution
        </p>
      </div>

      {/* Report types grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {reportTypes.map((report) => (
          <div key={report.id} className="card card-hover p-6">
            <div className="flex items-start gap-4">
              <div className={clsx("p-3 rounded-xl", report.color)}>
                <report.icon className="w-6 h-6" />
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-brand-100 text-lg mb-1">{report.name}</h3>
                <p className="text-sm text-brand-400 mb-4">{report.description}</p>
                <button
                  onClick={() => handleDownload(report.id)}
                  disabled={downloading === report.id}
                  className="btn-secondary text-sm py-2 px-4 flex items-center gap-2"
                >
                  {downloading === report.id ? (
                    <>
                      <div className="animate-spin w-4 h-4 border-2 border-brand-400 border-t-transparent rounded-full" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Download className="w-4 h-4" />
                      Download PDF
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Custom reports section */}
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-4">
          <FileText className="w-6 h-6 text-gold-400" />
          <h2 className="text-xl font-semibold text-brand-100">Custom Reports</h2>
        </div>
        <p className="text-brand-400 mb-6">
          Need a customized report with specific data or formatting? Contact your administrator
          to request custom report templates.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-brand-800/30 rounded-xl p-4 border border-brand-700/50">
            <h4 className="font-medium text-brand-200 mb-1">Period Selection</h4>
            <p className="text-sm text-brand-500">Filter by custom date ranges</p>
          </div>
          <div className="bg-brand-800/30 rounded-xl p-4 border border-brand-700/50">
            <h4 className="font-medium text-brand-200 mb-1">Asset Filtering</h4>
            <p className="text-sm text-brand-500">Select specific holdings</p>
          </div>
          <div className="bg-brand-800/30 rounded-xl p-4 border border-brand-700/50">
            <h4 className="font-medium text-brand-200 mb-1">Benchmark Comparison</h4>
            <p className="text-sm text-brand-500">Compare against indices</p>
          </div>
        </div>
      </div>
    </div>
  );
}
