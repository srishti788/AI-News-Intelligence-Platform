import React from 'react';
import { LogOut, Settings, User } from 'lucide-react';

const Header = ({ user, demoMode, onLogout }) => {
  return (
    <header className="bg-gradient-to-r from-dark-900 to-dark-800 border-b border-glass-200 backdrop-blur-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-400 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">📰</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">News Intelligence</h1>
              <p className="text-xs text-gray-400">AI-Powered News Analytics</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {(user || demoMode) && (
              <>
                <div className="flex items-center gap-3 px-4 py-2 bg-glass-100 rounded-lg">
                  <User size={18} className="text-gray-400" />
                  <span className="text-white">{user?.email || 'Demo User'}</span>
                  {demoMode && <span className="text-xs text-blue-400">(Demo Mode)</span>}
                </div>
                <button className="p-2 hover:bg-glass-100 rounded-lg transition-colors text-gray-400 hover:text-white">
                  <Settings size={20} />
                </button>
                <button
                  onClick={onLogout}
                  className="p-2 hover:bg-red-900/20 rounded-lg transition-colors text-gray-400 hover:text-red-400"
                >
                  <LogOut size={20} />
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
