import React, { useState, useEffect } from 'react';
import {
  Users,
  AlertTriangle,
  Send,
  Sprout,
  ArrowRight,
  RefreshCw,
  MapPin,
  Play,
  Activity,
  CheckCircle,
  AlertCircle,
  XCircle,
  ShieldCheck,
  Clock,
} from 'lucide-react';
import StatCard from '../components/StatCard';
import RiskBadge from '../components/RiskBadge';
import WeatherCard from '../components/WeatherCard';
import { api } from '../api';

export default function Dashboard({ t, lang, setActiveTab, onOpenAlertModal }) {
  const [farmers, setFarmers] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [forecast, setForecast] = useState(null);
  const [selectedLocation, setSelectedLocation] = useState('Thanjavur');
  const [riskAssessment, setRiskAssessment] = useState(null);
  const [loading, setLoading] = useState(true);

  // Automatic Weather Risk Monitoring states
  const [monitoringLoading, setMonitoringLoading] = useState(false);
  const [monitoringSummary, setMonitoringSummary] = useState(null);
  const [monitoringFeedback, setMonitoringFeedback] = useState(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const [farmersData, alertsData, forecastData] = await Promise.all([
        api.getFarmers(),
        api.getAlertHistory(),
        api.getForecast(selectedLocation),
      ]);
      setFarmers(farmersData);
      setAlerts(alertsData);
      setForecast(forecastData);

      // Analyze for selected location
      const riskData = await api.analyzeRisk({
        location: selectedLocation,
        crop: 'Paddy',
        growth_stage: 'Flowering',
        forecast_data: forecastData,
      });
      setRiskAssessment(riskData);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedLocation]);

  const handleRunMonitoring = async () => {
    setMonitoringLoading(true);
    setMonitoringFeedback(null);
    try {
      const summary = await api.runMonitoring();
      setMonitoringSummary(summary);
      setMonitoringFeedback({
        type: 'success',
        message: `${t.monitoringComplete} (${summary.farmers_checked} ${t.summaryFarmersChecked.toLowerCase()}, ${summary.alerts_simulated} ${t.summaryAlertsSimulated.toLowerCase()})`,
      });
      // Refresh alert history and statistics to reflect newly generated warnings
      await loadData();
    } catch (err) {
      console.error('Monitoring cycle failed:', err);
      if (err.status === 409 || (err.message && err.message.toLowerCase().includes('in progress'))) {
        setMonitoringFeedback({
          type: 'warning',
          message: t.monitoringConflict,
        });
      } else {
        setMonitoringFeedback({
          type: 'error',
          message: t.monitoringError,
        });
      }
    } finally {
      setMonitoringLoading(false);
    }
  };

  return (
    <div>
      {/* Top Stats Grid */}
      <div className="grid-stats">
        <StatCard
          title={t.statFarmers}
          value={farmers.length}
          icon={Users}
          badgeText="Active in SQLite"
        />
        <StatCard
          title={t.statHighRisk}
          value={riskAssessment?.overall_risk === 'High' ? 1 : 0}
          icon={AlertTriangle}
          badgeText="Flowering Submergence Hazard"
        />
        <StatCard
          title={t.statAlertsSent}
          value={alerts.length}
          icon={Send}
          badgeText="Simulated + Logged"
        />
        <StatCard
          title={t.statActiveCrop}
          value={t.paddyCrop}
          icon={Sprout}
          badgeText="5 Growth Stages Configured"
        />
      </div>

      {/* Automated Weather Risk-Monitoring Action & Summary Panel */}
      <div className="card" style={{ marginBottom: '2rem', border: '1px solid var(--border-subtle)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <Activity size={22} color="var(--primary-400)" />
              <h2 className="card-title" style={{ marginBottom: 0 }}>
                {t.monitoringCardTitle}
              </h2>
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-dim)', marginTop: '0.35rem', maxWidth: '750px' }}>
              {t.monitoringCardSubtitle}
            </p>
          </div>

          <button
            className="btn btn-primary"
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.65rem 1.25rem', fontWeight: 600 }}
            onClick={handleRunMonitoring}
            disabled={monitoringLoading}
          >
            {monitoringLoading ? (
              <>
                <RefreshCw size={16} className="spin" />
                {t.monitoringInProgress}
              </>
            ) : (
              <>
                <Play size={16} />
                {t.runWeatherMonitoring}
              </>
            )}
          </button>
        </div>

        {/* Feedback Alert Banner */}
        {monitoringFeedback && (
          <div
            style={{
              marginTop: '1rem',
              padding: '0.75rem 1rem',
              borderRadius: 'var(--radius-sm)',
              display: 'flex',
              alignItems: 'center',
              gap: '0.6rem',
              fontSize: '0.88rem',
              fontWeight: 500,
              background:
                monitoringFeedback.type === 'success'
                  ? '#DCFCE7'
                  : monitoringFeedback.type === 'warning'
                  ? '#FEF3C7'
                  : '#FEE2E2',
              border: `1px solid ${
                monitoringFeedback.type === 'success'
                  ? '#86EFAC'
                  : monitoringFeedback.type === 'warning'
                  ? '#FCD34D'
                  : '#FCA5A5'
              }`,
              color:
                monitoringFeedback.type === 'success'
                  ? '#166534'
                  : monitoringFeedback.type === 'warning'
                  ? '#92400E'
                  : '#991B1B',
            }}
          >
            {monitoringFeedback.type === 'success' && <CheckCircle size={18} color="#166534" />}
            {monitoringFeedback.type === 'warning' && <AlertCircle size={18} color="#92400E" />}
            {monitoringFeedback.type === 'error' && <XCircle size={18} color="#991B1B" />}
            <span>{monitoringFeedback.message}</span>
          </div>
        )}

        {/* Monitoring Summary Metrics Grid */}
        {monitoringSummary && (
          <div
            style={{
              marginTop: '1.25rem',
              padding: '1.25rem',
              background: '#F8FAFC',
              borderRadius: 'var(--radius-md)',
              border: '1px solid #E2E8F0',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div style={{ fontWeight: 700, fontSize: '0.95rem', color: '#1F2937', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Clock size={16} color="#166534" />
                {t.monitoringSummaryTitle}
              </div>
              <span style={{ fontSize: '0.8rem', color: '#64748B' }}>
                {t.lastRunAt}: {new Date().toLocaleTimeString()} • {monitoringSummary.cycle_duration_seconds}s
              </span>
            </div>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))',
                gap: '0.85rem',
              }}
            >
              {/* 1. Farmers Checked */}
              <div style={{ padding: '0.85rem', background: '#FFFFFF', borderRadius: 'var(--radius-sm)', border: '1px solid #E2E8F0' }}>
                <div style={{ fontSize: '0.78rem', color: '#64748B', display: 'flex', alignItems: 'center', gap: '0.4rem', fontWeight: 500 }}>
                  <Users size={14} color="#166534" />
                  {t.summaryFarmersChecked}
                </div>
                <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#1F2937', marginTop: '0.3rem' }}>
                  {monitoringSummary.farmers_checked}
                </div>
              </div>

              {/* 2. Risks Detected */}
              <div style={{ padding: '0.85rem', background: '#FFFFFF', borderRadius: 'var(--radius-sm)', border: '1px solid #E2E8F0' }}>
                <div style={{ fontSize: '0.78rem', color: '#64748B', display: 'flex', alignItems: 'center', gap: '0.4rem', fontWeight: 500 }}>
                  <AlertTriangle size={14} color="#D97706" />
                  {t.summaryRisksDetected}
                </div>
                <div style={{ fontSize: '1.4rem', fontWeight: 700, color: monitoringSummary.risks_detected > 0 ? '#B45309' : '#1F2937', marginTop: '0.3rem' }}>
                  {monitoringSummary.risks_detected}
                </div>
              </div>

              {/* 3. Simulated SMS Alerts (Demo only - not delivered) */}
              <div style={{ padding: '0.85rem', background: '#FFFFFF', borderRadius: 'var(--radius-sm)', border: '1px solid #E2E8F0' }}>
                <div style={{ fontSize: '0.78rem', color: '#64748B', display: 'flex', alignItems: 'center', gap: '0.4rem', fontWeight: 500 }}>
                  <Send size={14} color="#0F766E" />
                  {t.summaryAlertsSimulated}
                </div>
                <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#0F766E', marginTop: '0.3rem' }}>
                  {monitoringSummary.alerts_simulated}
                </div>
                <div style={{ marginTop: '0.35rem' }}>
                  <span
                    style={{
                      fontSize: '0.7rem',
                      fontWeight: 600,
                      padding: '0.15rem 0.45rem',
                      borderRadius: '4px',
                      background: '#FEF3C7',
                      color: '#92400E',
                      border: '1px solid #FCD34D',
                      display: 'inline-block',
                    }}
                  >
                    {t.demoOnlyBadge}
                  </span>
                </div>
              </div>

              {/* 4. Genuinely Sent Alerts */}
              <div style={{ padding: '0.85rem', background: '#FFFFFF', borderRadius: 'var(--radius-sm)', border: '1px solid #E2E8F0' }}>
                <div style={{ fontSize: '0.78rem', color: '#64748B', display: 'flex', alignItems: 'center', gap: '0.4rem', fontWeight: 500 }}>
                  <CheckCircle size={14} color="#166534" />
                  {t.summaryAlertsSent}
                </div>
                <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#166534', marginTop: '0.3rem' }}>
                  {monitoringSummary.alerts_sent}
                </div>
                <div style={{ fontSize: '0.7rem', color: '#64748B', marginTop: '0.35rem' }}>
                  Live gateway dispatches
                </div>
              </div>

              {/* 5. Duplicate Alerts Suppressed */}
              <div style={{ padding: '0.85rem', background: '#FFFFFF', borderRadius: 'var(--radius-sm)', border: '1px solid #E2E8F0' }}>
                <div style={{ fontSize: '0.78rem', color: '#64748B', display: 'flex', alignItems: 'center', gap: '0.4rem', fontWeight: 500 }}>
                  <ShieldCheck size={14} color="#0F766E" />
                  {t.summaryDuplicatesSuppressed}
                </div>
                <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#1F2937', marginTop: '0.3rem' }}>
                  {monitoringSummary.duplicates_suppressed}
                </div>
                <div style={{ fontSize: '0.7rem', color: '#64748B', marginTop: '0.35rem' }}>
                  24-hour guard active
                </div>
              </div>

              {/* 6. Failures */}
              <div style={{ padding: '0.85rem', background: '#FFFFFF', borderRadius: 'var(--radius-sm)', border: '1px solid #E2E8F0' }}>
                <div style={{ fontSize: '0.78rem', color: '#64748B', display: 'flex', alignItems: 'center', gap: '0.4rem', fontWeight: 500 }}>
                  <XCircle size={14} color="#DC2626" />
                  {t.summaryFailures}
                </div>
                <div style={{ fontSize: '1.4rem', fontWeight: 700, color: monitoringSummary.failures > 0 ? '#991B1B' : '#1F2937', marginTop: '0.3rem' }}>
                  {monitoringSummary.failures}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Main 2-Column Section */}
      <div className="grid-2col" style={{ marginBottom: '2rem' }}>
        {/* Weather & Active Hazard Panel */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2 className="card-title" style={{ marginBottom: 0 }}>
              <MapPin size={20} color="var(--primary-400)" />
              {t.weatherOverview}
            </h2>
            <select
              className="form-select"
              style={{ width: 'auto', padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}
              value={selectedLocation}
              onChange={(e) => setSelectedLocation(e.target.value)}
            >
              <option value="Thanjavur">Thanjavur (Delta Hub)</option>
              <option value="Madurai">Madurai (Southern)</option>
              <option value="Tiruchirappalli">Tiruchirappalli</option>
              <option value="Thiruvarur">Thiruvarur</option>
              <option value="Coimbatore">Coimbatore</option>
            </select>
          </div>

          <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.5rem' }}>
            {forecast?.source} • {forecast?.period}
          </div>

          {forecast?.daily_forecasts && (
            <div className="forecast-strip">
              {forecast.daily_forecasts.map((day) => (
                <WeatherCard key={day.date} day={day} />
              ))}
            </div>
          )}

          {/* Quick Risk Indicator */}
          {riskAssessment && (
            <div
              style={{
                marginTop: '1.25rem',
                padding: '1rem',
                borderRadius: 'var(--radius-sm)',
                background: 'var(--bg-surface-elevated)',
                border: '1px solid var(--border-subtle)',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>
                    {t.paddyCrop} (
                    {lang === 'ta' ? 'பூக்கும் பருவம்' : 'Flowering Stage'})
                  </span>
                  <div style={{ fontWeight: 600, fontSize: '1.05rem', color: 'var(--text-main)', marginTop: '0.2rem' }}>
                    {selectedLocation} Risk Assessment
                  </div>
                </div>
                <RiskBadge level={riskAssessment.overall_risk} t={t} />
              </div>

              <div style={{ marginTop: '0.75rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                {lang === 'ta'
                  ? riskAssessment.hazards[0]?.reason_ta
                  : riskAssessment.hazards[0]?.reason_en}
              </div>

              <div style={{ marginTop: '1rem', display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                <button
                  className="btn btn-primary btn-sm"
                  onClick={() => setActiveTab('risk')}
                >
                  {t.quickRiskAssessment} <ArrowRight size={14} />
                </button>
                <button
                  className="btn btn-outline btn-sm"
                  onClick={() =>
                    onOpenAlertModal({
                      hazard: riskAssessment.hazards[0]?.hazard || 'Heavy Rainfall',
                      riskLevel: riskAssessment.overall_risk,
                      triggerValue: riskAssessment.hazards[0]?.trigger_value || '',
                    })
                  }
                >
                  <Send size={14} /> {t.triggerWarningAlert}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Recent Alerts Feed */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2 className="card-title" style={{ marginBottom: 0 }}>
              <Send size={20} color="var(--primary-400)" />
              {t.recentAlerts}
            </h2>
            <button
              className="btn btn-outline btn-sm"
              onClick={() => setActiveTab('history')}
            >
              {t.viewAllAlerts}
            </button>
          </div>

          {alerts.length === 0 ? (
            <div style={{ padding: '2rem 1rem', textAlign: 'center', color: 'var(--text-dim)' }}>
              {t.noAlertsYet}
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table">
                <thead>
                  <tr>
                    <th>{t.colFarmer}</th>
                    <th>{t.colHazard}</th>
                    <th>{t.colRisk}</th>
                    <th>{t.colStatus}</th>
                  </tr>
                </thead>
                <tbody>
                  {alerts.slice(0, 5).map((alert) => (
                    <tr key={alert.id}>
                      <td>
                        <div style={{ fontWeight: 600 }}>{alert.farmer_name}</div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                          {alert.location} • {alert.growth_stage}
                        </div>
                      </td>
                      <td>{alert.hazard}</td>
                      <td>
                        <RiskBadge level={alert.risk_level} t={t} showIcon={false} />
                      </td>
                      <td>
                        <span
                          style={{
                            fontSize: '0.75rem',
                            padding: '0.2rem 0.55rem',
                            borderRadius: '4px',
                            background: alert.status === 'SIMULATED' ? '#FEF3C7' : '#DCFCE7',
                            border: `1px solid ${alert.status === 'SIMULATED' ? '#FCD34D' : '#86EFAC'}`,
                            color: alert.status === 'SIMULATED' ? '#92400E' : '#166534',
                            fontWeight: 700,
                          }}
                        >
                          {alert.status === 'SIMULATED' ? 'SIMULATED (Demo)' : alert.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Registered Farmers Preview */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 className="card-title" style={{ marginBottom: 0 }}>
            <Users size={20} color="var(--primary-400)" />
            {t.farmerListTitle}
          </h2>
          <button
            className="btn btn-primary btn-sm"
            onClick={() => setActiveTab('registration')}
          >
            {t.registerBtn}
          </button>
        </div>

        {farmers.length === 0 ? (
          <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-dim)' }}>
            {t.noFarmersYet}
          </div>
        ) : (
          <div className="table-responsive">
            <table className="table">
              <thead>
                <tr>
                  <th>{t.farmerName}</th>
                  <th>{t.mobileNumber}</th>
                  <th>{t.locationDistrict}</th>
                  <th>{t.cropType}</th>
                  <th>{t.growthStage}</th>
                  <th>{t.prefLang}</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {farmers.slice(0, 6).map((f) => (
                  <tr key={f.id}>
                    <td style={{ fontWeight: 600 }}>{f.name}</td>
                    <td style={{ fontFamily: 'monospace' }}>{f.mobile_number}</td>
                    <td>{f.location}</td>
                    <td>{f.crop}</td>
                    <td>
                      <span style={{ color: '#0F766E', fontWeight: 600 }}>{f.growth_stage}</span>
                    </td>
                    <td>
                      <span className="demo-pill" style={{ textTransform: 'uppercase' }}>
                        {f.preferred_language === 'ta' ? 'தமிழ்' : 'English'}
                      </span>
                    </td>
                    <td>
                      <button
                        className="btn btn-outline btn-sm"
                        onClick={() =>
                          onOpenAlertModal({
                            initialFarmerId: f.id,
                            hazard: 'Heavy Rainfall',
                            riskLevel: 'High',
                          })
                        }
                      >
                        <Send size={12} /> SMS
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
