import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import AlertModal from './components/AlertModal';
import Dashboard from './pages/Dashboard';
import RiskAnalysis from './pages/RiskAnalysis';
import FarmerRegistration from './pages/FarmerRegistration';
import AlertHistory from './pages/AlertHistory';
import Settings from './pages/Settings';
import { translations } from './i18n/translations';
import { api } from './api';
import { CheckCircle2, AlertCircle } from 'lucide-react';

export default function App() {
  const [lang, setLang] = useState(() => {
    return localStorage.getItem('tamilagri_lang') || 'ta';
  });
  const [activeTab, setActiveTab] = useState('dashboard');
  const [farmers, setFarmers] = useState([]);
  const [isDemo, setIsDemo] = useState(true);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    localStorage.setItem('tamilagri_lang', lang);
  }, [lang]);

  // Alert modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [modalConfig, setModalConfig] = useState({});
  const [isSendingAlert, setIsSendingAlert] = useState(false);

  const t = translations[lang] || translations.ta;

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4500);
  };

  const refreshFarmers = async () => {
    try {
      const data = await api.getFarmers();
      setFarmers(data);
    } catch (err) {
      console.error('Failed to refresh farmers:', err);
    }
  };

  useEffect(() => {
    refreshFarmers();
    api
      .getHealth()
      .then((data) => setIsDemo(data.demo_mode))
      .catch(() => setIsDemo(true));
  }, []);

  const handleOpenAlertModal = (config = {}) => {
    setModalConfig(config);
    setModalOpen(true);
  };

  const handleConfirmAlert = async (payload) => {
    setIsSendingAlert(true);
    try {
      const result = await api.sendAlert(payload);
      setModalOpen(false);
      const msg = t.dispatchToast
        ? t.dispatchToast
            .replace('{name}', result.farmer_name)
            .replace('{status}', result.status)
            .replace('{provider}', result.provider)
        : `Alert dispatched to ${result.farmer_name}! Status: [${result.status}] via ${result.provider} adapter.`;
      showToast(msg, 'success');
    } catch (err) {
      showToast(err.message || (lang === 'ta' ? 'எச்சரிக்கை அனுப்புவதில் பிழை ஏற்பட்டது' : 'Failed to dispatch alert'), 'error');
    } finally {
      setIsSendingAlert(false);
    }
  };

  return (
    <div>
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        lang={lang}
        setLang={setLang}
        t={t}
        isDemo={isDemo}
      />

      <main className="app-container">
        {activeTab === 'dashboard' && (
          <Dashboard
            t={t}
            lang={lang}
            setActiveTab={setActiveTab}
            onOpenAlertModal={handleOpenAlertModal}
          />
        )}

        {activeTab === 'risk' && (
          <RiskAnalysis
            t={t}
            lang={lang}
            farmers={farmers}
            onOpenAlertModal={handleOpenAlertModal}
          />
        )}

        {activeTab === 'registration' && (
          <FarmerRegistration
            t={t}
            lang={lang}
            onOpenAlertModal={handleOpenAlertModal}
            onFarmerUpdated={setFarmers}
          />
        )}

        {activeTab === 'history' && (
          <AlertHistory
            t={t}
            lang={lang}
          />
        )}

        {activeTab === 'settings' && (
          <Settings
            t={t}
            lang={lang}
            setLang={setLang}
            isDemo={isDemo}
          />
        )}
      </main>

      {/* Alert Trigger Modal */}
      <AlertModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        onConfirm={handleConfirmAlert}
        farmers={farmers}
        initialFarmerId={modalConfig.initialFarmerId}
        hazard={modalConfig.hazard || 'Heavy Rainfall'}
        riskLevel={modalConfig.riskLevel || 'High'}
        triggerValue={modalConfig.triggerValue || ''}
        t={t}
        isSending={isSendingAlert}
      />

      {/* Toast Notification */}
      {toast && (
        <div
          className="toast"
          style={{
            borderColor: toast.type === 'error' ? '#DC2626' : '#166534',
          }}
        >
          {toast.type === 'error' ? (
            <AlertCircle size={20} color="#DC2626" />
          ) : (
            <CheckCircle2 size={20} color="#166534" />
          )}
          <span>{toast.message}</span>
        </div>
      )}

      {/* Footer */}
      <footer
        style={{
          borderTop: '1px solid #E2E8F0',
          padding: '2rem 1.5rem',
          textAlign: 'center',
          fontSize: '0.85rem',
          color: '#CBD5E1',
          marginTop: '3rem',
        }}
      >
        <p>
          <strong>{t.projectTitle || 'TamilAgri AI'}</strong> — {t.footerTitle}
        </p>
        <p style={{ marginTop: '0.25rem' }}>
          {t.footerSubtitle}
        </p>
      </footer>
    </div>
  );
}
