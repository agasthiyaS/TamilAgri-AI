import React, { useState, useEffect } from 'react';
import { History, Filter, Eye, RefreshCw, X, MessageSquare, ShieldCheck } from 'lucide-react';
import RiskBadge from '../components/RiskBadge';
import { api } from '../api';

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
          <RefreshCw size={14} /> Refresh Logs
        </button>
      </div>

      {/* Filter Bar */}
      <div className="card" style={{ padding: '1rem 1.25rem', marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            <Filter size={16} /> Filters:
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
            <option value="SIMULATED">SIMULATED</option>
            <option value="DELIVERED">DELIVERED</option>
            <option value="FAILED">FAILED</option>
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
              Reset
            </button>
          )}
        </div>
      </div>

      {/* Log Table Card */}
      <div className="card">
        {loading ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-dim)' }}>Loading alert logs...</div>
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
                  <th>Actions</th>
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
                      {alert.location}
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                        {alert.crop} • {alert.growth_stage}
                      </div>
                    </td>
                    <td style={{ fontWeight: 500 }}>{alert.hazard}</td>
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
                          padding: '0.25rem 0.5rem',
                          borderRadius: '4px',
                          background:
                            alert.status === 'SIMULATED'
                              ? 'rgba(245, 158, 11, 0.15)'
                              : alert.status === 'DELIVERED'
                              ? 'rgba(16, 185, 129, 0.15)'
                              : 'rgba(239, 68, 68, 0.15)',
                          color:
                            alert.status === 'SIMULATED'
                              ? '#f59e0b'
                              : alert.status === 'DELIVERED'
                              ? '#10b981'
                              : '#ef4444',
                          fontWeight: 700,
                        }}
                      >
                        {alert.status}
                      </span>
                    </td>
                    <td style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>
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
              <h3 style={{ fontSize: '1.2rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <MessageSquare size={18} color="var(--primary-400)" />
                SMS Payload Details (Alert #{selectedAlert.id})
              </h3>
              <button
                onClick={() => setSelectedAlert(null)}
                style={{ background: 'none', border: 'none', color: 'var(--text-dim)', cursor: 'pointer' }}
              >
                <X size={20} />
              </button>
            </div>

            <div style={{ marginBottom: '1rem', fontSize: '0.85rem', color: 'var(--text-dim)' }}>
              Recipient: <strong style={{ color: 'var(--text-main)' }}>{selectedAlert.farmer_name}</strong> ({selectedAlert.mobile_number}) • Gateway: <code>{selectedAlert.provider}</code> (ID: {selectedAlert.provider_message_id || 'N/A'})
            </div>

            <div
              style={{
                background: 'rgba(6, 23, 18, 0.85)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-sm)',
                padding: '1.25rem',
                fontFamily: 'monospace',
                fontSize: '0.9rem',
                whiteSpace: 'pre-wrap',
                lineHeight: 1.6,
                color: '#e2e8f0',
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
