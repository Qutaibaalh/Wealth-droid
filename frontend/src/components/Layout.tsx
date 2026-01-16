import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, 
  TrendingUp, 
  Landmark, 
  Building2, 
  Briefcase,
  FileText,
  Upload,
  LogOut,
  User
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import clsx from 'clsx';

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/equities', icon: TrendingUp, label: 'Equities' },
  { to: '/fixed-income', icon: Landmark, label: 'Fixed Income' },
  { to: '/real-estate', icon: Building2, label: 'Real Estate' },
  { to: '/private-funds', icon: Briefcase, label: 'Private Funds' },
  { to: '/reports', icon: FileText, label: 'Reports' },
  { to: '/import', icon: Upload, label: 'Import Data' },
];

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="w-72 bg-brand-900/80 backdrop-blur-xl border-r border-brand-800/50 flex flex-col">
        {/* Logo */}
        <div className="p-6 border-b border-brand-800/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gold-500 rounded-xl flex items-center justify-center">
              <span className="font-display font-bold text-brand-950 text-xl">A</span>
            </div>
            <div>
              <h1 className="font-display font-semibold text-brand-50">ALrashid</h1>
              <p className="text-xs text-brand-500">Family Office</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                clsx('nav-link', isActive && 'active')
              }
            >
              <item.icon className="w-5 h-5" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        {/* User section */}
        <div className="p-4 border-t border-brand-800/50">
          <div className="flex items-center gap-3 px-4 py-3">
            <div className="w-10 h-10 bg-brand-800 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-brand-400" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-brand-100 truncate">
                {user?.full_name}
              </p>
              <p className="text-xs text-brand-500 capitalize">
                {user?.role.replace('_', ' ')}
              </p>
            </div>
            <button
              onClick={handleLogout}
              className="p-2 hover:bg-brand-800 rounded-lg transition-colors"
              title="Logout"
            >
              <LogOut className="w-4 h-4 text-brand-400" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
