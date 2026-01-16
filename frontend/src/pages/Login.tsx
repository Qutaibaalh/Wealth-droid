import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Eye, EyeOff, Lock, User } from 'lucide-react';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid username or password');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left side - decorative */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-brand-900 via-brand-950 to-black relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-gold-500/5 via-transparent to-gold-500/5 opacity-50" />
        
        <div className="relative z-10 flex flex-col justify-center px-16">
          <div className="mb-8">
            <div className="w-16 h-16 bg-gold-500 rounded-2xl flex items-center justify-center mb-6 glow">
              <span className="font-display font-bold text-brand-950 text-3xl">A</span>
            </div>
            <h1 className="font-display text-5xl font-bold text-brand-50 mb-4">
              ALrashid
              <br />
              <span className="text-gradient">Family Office</span>
            </h1>
            <p className="text-brand-400 text-lg max-w-md">
              Comprehensive portfolio management for multi-generational wealth preservation and growth.
            </p>
          </div>
          
          <div className="grid grid-cols-2 gap-6 max-w-md">
            <div className="card p-4">
              <p className="stat-value text-2xl">300+</p>
              <p className="stat-label text-xs">Real Estate Units</p>
            </div>
            <div className="card p-4">
              <p className="stat-value text-2xl">30+</p>
              <p className="stat-label text-xs">Fund Investments</p>
            </div>
          </div>
        </div>
      </div>

      {/* Right side - login form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <div className="lg:hidden mb-8 text-center">
            <div className="w-14 h-14 bg-gold-500 rounded-xl flex items-center justify-center mx-auto mb-4">
              <span className="font-display font-bold text-brand-950 text-2xl">A</span>
            </div>
            <h1 className="font-display text-2xl font-bold text-brand-50">ALrashid Family Office</h1>
          </div>

          <div className="card p-8">
            <h2 className="text-2xl font-display font-semibold text-brand-50 mb-2">Welcome back</h2>
            <p className="text-brand-400 mb-8">Sign in to access your portfolio</p>

            <form onSubmit={handleSubmit} className="space-y-6">
              {error && (
                <div className="bg-rose-500/10 border border-rose-500/30 text-rose-400 px-4 py-3 rounded-xl text-sm">
                  {error}
                </div>
              )}

              <div>
                <label htmlFor="username" className="label">Username</label>
                <div className="relative">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-brand-500" />
                  <input
                    id="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="input w-full pl-12"
                    placeholder="Enter your username"
                    required
                  />
                </div>
              </div>

              <div>
                <label htmlFor="password" className="label">Password</label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-brand-500" />
                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="input w-full pl-12 pr-12"
                    placeholder="Enter your password"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-brand-500 hover:text-brand-300"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary w-full flex items-center justify-center"
              >
                {isLoading ? (
                  <span className="animate-pulse">Signing in...</span>
                ) : (
                  'Sign In'
                )}
              </button>
            </form>
          </div>

          <p className="text-center text-brand-500 text-sm mt-6">
            Secure access for authorized users only
          </p>
        </div>
      </div>
    </div>
  );
}
