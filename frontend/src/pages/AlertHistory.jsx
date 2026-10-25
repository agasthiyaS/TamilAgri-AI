import React, { useState, useEffect } from 'react';
import { History, Filter, Eye, RefreshCw, X, MessageSquare, ShieldCheck } from 'lucide-react';
import RiskBadge from '../components/RiskBadge';
import { api } from '../api';
import {
  translateLocation,
  translateGrowthStage,
  translateHazard,
  translateStatus,
  translateCrop,
} from '../i18n/translations';

export default function AlertHistory({ t, lang }) {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedAlert, setSelectedAlert] = useState(null);

  // Filters
  const [filterHazard, setFilterHazard] = useState('');
  const [filterRisk, setFilterRisk] = useState('');
  const [filterStatus, setFilterStatus] = useState('');

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await api.getAlertHistory({
        hazard: filterHazard || undefined,
        risk_level: filterRisk || undefined,
        status: filterStatus || undefined,
      });
      setAlerts(data);
    } catch (err) {
      console.error('Failed to load alert history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [filterHazard, filterRisk, filterStatus]);

  const formatDate = (isoString) => {
    try {
      const d = new Date(isoString);
      return d.toLocaleString(lang === 'ta' ? 'ta-IN' : 'en-US', {
        dateStyle: 'medium',
        timeStyle: 'short',
      });
    } catch {
      return isoString;
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.25rem' }}>
            {t.historyTitle}
          </h1>
          <p style={{ color: 'var(--text-dim)', fontSize: '0.95rem' }}>{t.historySubtitle}</p>
        </div>

        <button className="btn btn-outline btn-sm" onClick={fetchHistory} disabled={loading}>
          <RefreshCw size={14} /> {t.refreshLogsBtn}
        </button>
      </div>

      {/* Filter Bar */}
      <div className="card" style={{ padding: '1rem 1.25rem', marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            <Filter size={16} /> {t.filterLabel}
          </div>

          <select
            className="form-select"
            style={{ width: 'auto', padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}
            value={filterHazard}
            onChange={(e) => setFilterHazard(e.target.value)}
          >
            <option value="">{t.filterHazard}</option>
            <option value="Heavy Rainfall">{t.hazardRain}</option>
            <option value="Extreme Heat">{t.hazardHeat}</option>
          </select>

          <select
            className="form-select"
            style={{ width: 'auto', padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}
            value={filterRisk}
            onChange={(e) => setFilterRisk(e.target.value)}
          >
            <option value="">{t.filterRisk}</option>
            <option value="High">{t.riskHigh}</option>
            <option value="Medium">{t.riskMedium}</option>
            <option value="Low">{t.riskLow}</option>
          </select>

          <select
            className="form-select"
            style={{ width: 'auto', padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
          >
            <option value="">{t.filterStatus}</option>
            <option value="SIMULATED">{translateStatus('SIMULATED', lang)}</option>
            <option value="DELIVERED">{translateStatus('DELIVERED', lang)}</option>
            <option value="FAILED">{translateStatus('FAILED', lang)}</option>
          </select>

          {(filterHazard || filterRisk || filterStatus) && (
            <button
              className="btn btn-outline btn-sm"
              onClick={() => {
                setFilterHazard('');
                setFilterRisk('');
                setFilterStatus('');
              }}
            >
              {t.resetBtn}
            </button>
          )}
        </div>
      </div>

      {/* Log Table Card */}
      <div className="card">
        {loading ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-dim)' }}>{t.loadingLogs}</div>
        ) : alerts.length === 0 ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-dim)' }}>{t.noAlertsYet}</div>
        ) : (
          <div className="table-responsive">
            <table className="table">
              <thead>
                <tr>
                  <th>{t.colFarmer}</th>
                  <th>{t.colLocation}</th>
                  <th>{t.colHazard}</th>
                  <th>{t.colRisk}</th>
                  <th>{t.colLang}</th>
                  <th>{t.colStatus}</th>
                  <th>{t.colSentAt}</th>
                  <th>{t.colActions}</th>
                </tr>
              </thead>
              <tbody>
                {alerts.map((alert) => (
                  <tr key={alert.id}>
                    <td>
                      <div style={{ fontWeight: 600 }}>{alert.farmer_name}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', fontFamily: 'monospace' }}>
                        {alert.mobile_number}
                      </div>
                    </td>
                    <td>
                      {translateLocation(alert.location, lang)}
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                        {translateCrop(alert.crop, lang)} • {translateGrowthStage(alert.growth_stage, lang)}
                      </div>
                    </td>
                    <td style={{ fontWeight: 500 }}>{translateHazard(alert.hazard, lang)}</td>
                    <td>
                      <RiskBadge level={alert.risk_level} t={t} showIcon={false} />
                    </td>
                    <td>
                      <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>
                        {alert.language === 'ta' ? 'தமிழ்' : 'EN'}
                      </span>
                    </td>
                    <td>
                      <span
                        style={{
                          fontSize: '0.75rem',
                          padding: '0.25rem 0.55rem',
                          borderRadius: '4px',
                          background:
                            alert.status === 'SIMULATED'
                              ? '#FEF3C7'
                              : alert.status === 'DELIVERED'
                              ? '#DCFCE7'
                              : '#FEE2E2',
                          border: `1px solid ${
                            alert.status === 'SIMULATED'
                              ? '#FCD34D'
                              : alert.status === 'DELIVERED'
                              ? '#86EFAC'
                              : '#FCA5A5'
                          }`,
                          color:
                            alert.status === 'SIMULATED'
                              ? '#92400E'
                              : alert.status === 'DELIVERED'
                              ? '#166534'
                              : '#991B1B',
                          fontWeight: 700,
                        }}
                      >
                        {translateStatus(alert.status, lang)}
                      </span>
                    </td>
                    <td style={{ fontSize: '0.8rem', color: '#64748B' }}>
                      {formatDate(alert.sent_at)}
                    </td>
                    <td>
                      <button
                        className="btn btn-outline btn-sm"
                        onClick={() => setSelectedAlert(alert)}
                        style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}
                      >
                        <Eye size={13} /> {t.viewMessageBtn}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Message Viewer Modal */}
      {selectedAlert && (
        <div className="modal-overlay">
          <div className="modal-content" style={{ maxWidth: '520px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <h3 style={{ fontSize: '1.2rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#1F2937' }}>
                <MessageSquare size={18} color="#166534" />
                {t.smsPayloadTitle} (#{selectedAlert.id})
              </h3>
              <button
                onClick={() => setSelectedAlert(null)}
                style={{ background: 'none', border: 'none', color: '#64748B', cursor: 'pointer' }}
              >
                <X size={20} />
              </button>
            </div>

            <div style={{ marginBottom: '1rem', fontSize: '0.85rem', color: '#64748B' }}>
              {t.recipientLabel} <strong style={{ color: '#1F2937' }}>{selectedAlert.farmer_name}</strong> ({selectedAlert.mobile_number}) • {t.gatewayLabel} <code>{selectedAlert.provider}</code> (ID: {selectedAlert.provider_message_id || 'N/A'})
            </div>

            <div
              style={{
                background: '#F8FAFC',
                border: '1px solid #E2E8F0',
                borderRadius: 'var(--radius-sm)',
                padding: '1.25rem',
                fontFamily: 'monospace',
                fontSize: '0.9rem',
                whiteSpace: 'pre-wrap',
                lineHeight: 1.6,
                color: '#1F2937',
              }}
            >
              {selectedAlert.message}
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
              <button className="btn btn-primary btn-sm" onClick={() => setSelectedAlert(null)}>
                {t.close}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
