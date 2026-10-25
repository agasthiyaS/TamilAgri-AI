import React from 'react';
import { Sprout, LayoutDashboard, CloudSun, UserPlus, History, Settings as SettingsIcon } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, lang, setLang, t, isDemo }) {
  const navItems = [
    { id: 'dashboard', label: t.navDashboard, icon: LayoutDashboard },
    { id: 'risk', label: t.navRiskAnalysis, icon: CloudSun },
    { id: 'registration', label: t.navRegistration, icon: UserPlus },
    { id: 'history', label: t.navAlertHistory, icon: History },
    { id: 'settings', label: t.navSettings, icon: SettingsIcon },
  ];

  return (
    <header className="navbar">
      <div className="nav-inner">
        <div className="brand" onClick={() => setActiveTab('dashboard')}>
          <div className="brand-icon">
            <Sprout size={24} />
          </div>
          <div>
            <div className="brand-title">
              TamilAgri <span>AI</span>
            </div>
            <span className="brand-tag">{t.projectSubtitle}</span>
          </div>
        </div>

        <nav>
          <ul className="nav-links">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <li key={item.id}>
                  <button
                    className={`nav-btn ${isActive ? 'active' : ''}`}
                    onClick={() => setActiveTab(item.id)}
                  >
                    <Icon size={16} />
                    <span>{item.label}</span>
                  </button>
                </li>
              );
            })}
          </ul>
        </nav>

        <div className="nav-actions">
          {isDemo ? (
            <span className="demo-pill" title="Running in zero-cost Demo Mode without real SMS charges">
              ● {t.demoMode}
            </span>
          ) : (
            <span className="live-pill">
              ● {t.liveMode}
            </span>
          )}

          <div className="lang-toggle">
            <button
              className={`lang-btn ${lang === 'ta' ? 'active' : ''}`}
              onClick={() => setLang('ta')}
              title="தமிழ் மொழிக்கு மாற்றுக"
            >
              தமிழ்
            </button>
            <button
              className={`lang-btn ${lang === 'en' ? 'active' : ''}`}
              onClick={() => setLang('en')}
              title="Switch to English"
            >
              EN
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
