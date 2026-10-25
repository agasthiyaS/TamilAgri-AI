import React, { useState, useEffect } from 'react';
import { Users, AlertTriangle, Send, Sprout, ArrowRight, RefreshCw, MapPin } from 'lucide-react';
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

      // Analyze for delta hub
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

  const highRiskCount = alerts.filter((a) => a.risk_level === 'High').length;

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
                            padding: '0.2rem 0.5rem',
                            borderRadius: '4px',
                            background: alert.status === 'SIMULATED' ? 'rgba(245, 158, 11, 0.15)' : 'rgba(16, 185, 129, 0.15)',
                            color: alert.status === 'SIMULATED' ? '#f59e0b' : '#10b981',
                            fontWeight: 600,
                          }}
                        >
                          {alert.status}
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
                      <span style={{ color: 'var(--primary-400)' }}>{f.growth_stage}</span>
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
