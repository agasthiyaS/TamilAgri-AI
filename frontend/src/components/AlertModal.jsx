import React, { useState, useEffect } from 'react';
import { Send, X, AlertTriangle, ShieldCheck, MessageSquare } from 'lucide-react';
import RiskBadge from './RiskBadge';
import { api } from '../api';
import { translateHazard, translateLocation, translateGrowthStage } from '../i18n/translations';

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
  const [previewSMS, setPreviewSMS] = useState('');

  const isTamil = t.colFarmer === 'விவசாயி';
  const lang = isTamil ? 'ta' : 'en';

  const currentFarmer = farmers.find((f) => String(f.id) === String(selectedFarmerId));

  useEffect(() => {
    if (currentFarmer) {
      api
        .generateWarning({
          crop: currentFarmer.crop || 'Paddy',
          growth_stage: currentFarmer.growth_stage || 'Flowering',
          hazard,
          risk_level: riskLevel,
          language: currentFarmer.preferred_language || 'ta',
          trigger_value: triggerValue,
          farmer_name: currentFarmer.name,
          location: currentFarmer.location,
        })
        .then((res) => setPreviewSMS(res.sms_text))
        .catch((err) => console.error('Failed to preview SMS:', err));
    }
  }, [selectedFarmerId, hazard, riskLevel, triggerValue, currentFarmer]);

  if (!isOpen) return null;

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
              <option value="">{t.chooseFarmerOption}</option>
              {farmers.map((f) => (
                <option key={f.id} value={f.id}>
                  {f.name} ({translateLocation(f.location, lang)} - {translateGrowthStage(f.growth_stage, lang)} | {f.preferred_language === 'ta' ? 'தமிழ்' : 'English'})
                </option>
              ))}
            </select>
          </div>

          <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.25rem' }}>
            <div style={{ flex: 1 }}>
              <span className="form-label">{t.colHazard}</span>
              <div style={{ fontWeight: 600, color: 'var(--text-main)', marginTop: '0.25rem' }}>
                {translateHazard(hazard, lang)}
              </div>
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
              {t.customMessageLabel}
            </label>
            <textarea
              className="form-textarea"
              rows="2"
              placeholder={
                currentFarmer?.preferred_language === 'ta'
                  ? t.customMessagePlaceholderTa
                  : t.customMessagePlaceholderEn
              }
              value={customMessage}
              onChange={(e) => setCustomMessage(e.target.value)}
            />
          </div>

          {/* Live SMS Preview */}
          <div className="form-group">
            <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#166534' }}>
              <MessageSquare size={14} />
              {currentFarmer?.preferred_language === 'ta'
                ? t.tamilSmsPreviewTitle
                : t.englishSmsPreviewTitle}
            </label>
            <div
              style={{
                background: '#F8FAFC',
                border: '1px solid #E2E8F0',
                borderRadius: 'var(--radius-sm)',
                padding: '0.95rem',
                fontSize: '0.85rem',
                fontFamily: 'monospace',
                whiteSpace: 'pre-wrap',
                lineHeight: 1.55,
                color: '#1F2937',
              }}
            >
              {customMessage.trim() ? customMessage : previewSMS || t.generatingPreview}
            </div>
          </div>

          <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input
              type="checkbox"
              id="forceResend"
              checked={forceResend}
              onChange={(e) => setForceResend(e.target.checked)}
              style={{ width: '16px', height: '16px', accentColor: '#166534' }}
            />
            <label htmlFor="forceResend" style={{ fontSize: '0.85rem', color: '#64748B', cursor: 'pointer' }}>
              {t.forceResendLabel}
            </label>
          </div>

          <div className="disclaimer-banner" style={{ margin: '1rem 0' }}>
            <ShieldCheck size={20} style={{ flexShrink: 0 }} />
            <div>
              <strong>{t.demoMode}:</strong> {t.demoGatewayNotice}
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
