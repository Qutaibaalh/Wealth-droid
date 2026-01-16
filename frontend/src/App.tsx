import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Equities from './pages/Equities';
import FixedIncome from './pages/FixedIncome';
import RealEstate from './pages/RealEstate';
import PrivateFunds from './pages/PrivateFunds';
import Reports from './pages/Reports';
import Import from './pages/Import';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-gold-400">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

export default function App() {
  const { checkAuth } = useAuth();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="equities" element={<Equities />} />
          <Route path="fixed-income" element={<FixedIncome />} />
          <Route path="real-estate" element={<RealEstate />} />
          <Route path="private-funds" element={<PrivateFunds />} />
          <Route path="reports" element={<Reports />} />
          <Route path="import" element={<Import />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
