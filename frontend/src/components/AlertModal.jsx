import React, { useState } from 'react';
import { Send, X, AlertTriangle, ShieldCheck } from 'lucide-react';
import RiskBadge from './RiskBadge';

export default function AlertModal({
  isOpen,
  onClose,
  onConfirm,
  farmers = [],
  initialFarmerId = null,
  hazard = 'Heavy Rainfall',
  riskLevel = 'High',
  triggerValue = '',
  t,
  isSending = false,
}) {
  const [selectedFarmerId, setSelectedFarmerId] = useState(
    initialFarmerId || (farmers.length > 0 ? farmers[0].id : '')
  );
  const [forceResend, setForceResend] = useState(false);
  const [customMessage, setCustomMessage] = useState('');

  if (!isOpen) return null;

  const currentFarmer = farmers.find((f) => String(f.id) === String(selectedFarmerId));

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedFarmerId) return;
    onConfirm({
      farmer_id: parseInt(selectedFarmerId, 10),
      hazard,
      risk_level: riskLevel,
      trigger_value: triggerValue,
      custom_message: customMessage.trim() ? customMessage : null,
      force_resend: forceResend,
    });
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Send size={20} color="var(--primary-400)" />
            {t.triggerWarningAlert}
          </h3>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', color: 'var(--text-dim)', cursor: 'pointer' }}
          >
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">{t.colFarmer}</label>
            <select
              className="form-select"
              value={selectedFarmerId}
              onChange={(e) => setSelectedFarmerId(e.target.value)}
              required
            >
              <option value="">-- Choose registered farmer --</option>
              {farmers.map((f) => (
                <option key={f.id} value={f.id}>
                  {f.name} ({f.location} - {f.growth_stage} | {f.preferred_language === 'ta' ? 'தமிழ்' : 'English'})
                </option>
              ))}
            </select>
          </div>

          <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.25rem' }}>
            <div style={{ flex: 1 }}>
              <span className="form-label">{t.colHazard}</span>
              <div style={{ fontWeight: 600, color: 'var(--text-main)', marginTop: '0.25rem' }}>{hazard}</div>
            </div>
            <div style={{ flex: 1 }}>
              <span className="form-label">{t.colRisk}</span>
              <div style={{ marginTop: '0.25rem' }}>
                <RiskBadge level={riskLevel} t={t} />
              </div>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">
              Optional Custom Message Override (Leave blank for automated bilingual template)
            </label>
            <textarea
              className="form-textarea"
              rows="3"
              placeholder={
                currentFarmer?.preferred_language === 'ta'
                  ? 'தானியங்கி தமிழ் மாதிரி செய்தி பயன்படுத்தப்படும்...'
                  : 'Automatic English SMS template will be formatted...'
              }
              value={customMessage}
              onChange={(e) => setCustomMessage(e.target.value)}
            />
          </div>

          <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input
              type="checkbox"
              id="forceResend"
              checked={forceResend}
              onChange={(e) => setForceResend(e.target.checked)}
              style={{ width: '16px', height: '16px', accentColor: 'var(--primary-500)' }}
            />
            <label htmlFor="forceResend" style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', cursor: 'pointer' }}>
              {t.forceResendLabel}
            </label>
          </div>

          <div className="disclaimer-banner" style={{ margin: '1rem 0' }}>
            <ShieldCheck size={20} style={{ flexShrink: 0 }} />
            <div>
              <strong>DEMO GATEWAY:</strong> Simulated dispatch will be logged in the database without carrier SMS charges.
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.5rem' }}>
            <button type="button" className="btn btn-outline" onClick={onClose} disabled={isSending}>
              {t.cancel}
            </button>
            <button type="submit" className="btn btn-primary" disabled={isSending || !selectedFarmerId}>
              {isSending ? t.sending : t.confirmSend}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
