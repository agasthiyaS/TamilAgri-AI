import React, { useState, useEffect } from 'react';
import { CloudSun, Send, ShieldAlert, AlertCircle, Info, CheckCircle2, ChevronRight, Languages } from 'lucide-react';
import RiskBadge from '../components/RiskBadge';
import WeatherCard from '../components/WeatherCard';
import { api } from '../api';

const TN_DISTRICTS = [
  'Thanjavur',
  'Madurai',
  'Tiruchirappalli',
  'Thiruvarur',
  'Nagapattinam',
  'Coimbatore',
  'Cuddalore',
  'Salem',
  'Tirunelveli',
];

const PADDY_STAGES = [
  { id: 'Nursery', en: 'Nursery (Seedling emergence)', ta: 'நாற்றங்கால் பருவம்' },
  { id: 'Tillering', en: 'Tillering (Vegetative branching)', ta: 'தூர் கட்டும் பருவம்' },
  { id: 'Flowering', en: 'Flowering (Anthesis & Pollination)', ta: 'பூக்கும் பருவம்' },
  { id: 'Grain filling', en: 'Grain filling (Milk & Dough stage)', ta: 'பால் பிடிக்கும் / மணி முதிரும் பருவம்' },
  { id: 'Harvest', en: 'Harvest (Ripening & Threshing)', ta: 'அறுவடைப் பருவம்' },
];

export default function RiskAnalysis({ t, lang, onOpenAlertModal, farmers = [] }) {
  const [location, setLocation] = useState('Thanjavur');
  const [customLocation, setCustomLocation] = useState('');
  const [stage, setStage] = useState('Flowering');
  const [forecast, setForecast] = useState(null);
  const [riskResult, setRiskResult] = useState(null);
  const [warningReport, setWarningReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const activeLocation = customLocation.trim() || location;

  const handleEvaluate = async () => {
    setLoading(true);
    setError(null);
    try {
      const forecastData = await api.getForecast(activeLocation);
      setForecast(forecastData);

      const result = await api.analyzeRisk({
        location: activeLocation,
        crop: 'Paddy',
        growth_stage: stage,
        forecast_data: forecastData,
      });
      setRiskResult(result);
    } catch (err) {
      setError(err.message || 'Failed to evaluate climate risk');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleEvaluate();
  }, [location, stage]);

  useEffect(() => {
    if (riskResult) {
      const primaryHazard = riskResult.hazards[0];
      const precaution = lang === 'ta' ? primaryHazard?.precaution_ta : primaryHazard?.precaution_en;
      api
        .generateWarning({
          crop: riskResult.crop,
          growth_stage: riskResult.growth_stage,
          hazard: primaryHazard?.hazard || 'Heavy Rainfall',
          risk_level: riskResult.overall_risk,
          language: lang,
          trigger_value: primaryHazard?.trigger_value,
          precaution: precaution,
          location: activeLocation,
        })
        .then(setWarningReport)
        .catch((err) => console.error('Failed to generate warning narrative:', err));
    }
  }, [riskResult, lang, activeLocation]);

  const matchingFarmers = farmers.filter(
    (f) =>
      f.location.toLowerCase().includes(activeLocation.toLowerCase()) ||
      activeLocation.toLowerCase().includes(f.location.toLowerCase())
  );

  return (
    <div>
      <div style={{ marginBottom: '1.5rem' }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.25rem' }}>
          {t.riskTitle}
        </h1>
        <p style={{ color: 'var(--text-dim)', fontSize: '0.95rem' }}>{t.riskSubtitle}</p>
      </div>

      {/* TNAU Agricultural Verification Notice Banner */}
      <div className="disclaimer-banner">
        <Info size={20} style={{ flexShrink: 0 }} />
        <div>
          <strong>{t.disclaimerTitle}:</strong> {t.disclaimerText}
        </div>
      </div>

      {error && (
        <div style={{ padding: '0.9rem 1.25rem', background: '#FEE2E2', border: '1px solid #FCA5A5', borderRadius: '8px', color: '#991B1B', fontWeight: 500, marginBottom: '1.5rem' }}>
          {error}
        </div>
      )}

      {/* Input Controls Card */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="grid-2col">
          {/* Location selector */}
          <div className="form-group">
            <label className="form-label">{t.selectLocation}</label>
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <select
                className="form-select"
                value={location}
                onChange={(e) => {
                  setLocation(e.target.value);
                  setCustomLocation('');
                }}
              >
                {TN_DISTRICTS.map((dist) => (
                  <option key={dist} value={dist}>
                    {dist}
                  </option>
                ))}
              </select>
            </div>
            <input
              type="text"
              className="form-input"
              placeholder="Or enter any Tamil Nadu district/taluk name..."
              value={customLocation}
              onChange={(e) => setCustomLocation(e.target.value)}
            />
          </div>

          {/* Growth Stage selector */}
          <div className="form-group">
            <label className="form-label">{t.selectStage}</label>
            <select
              className="form-select"
              value={stage}
              onChange={(e) => setStage(e.target.value)}
            >
              {PADDY_STAGES.map((s) => (
                <option key={s.id} value={s.id}>
                  {lang === 'ta' ? s.ta : s.en}
                </option>
              ))}
            </select>
            <div className="form-help">
              Crop: <strong>Paddy (Oryza sativa)</strong> • Evaluated against rain & heat thresholds
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.5rem' }}>
          <button
            className="btn btn-primary"
            onClick={handleEvaluate}
            disabled={loading}
          >
            <CloudSun size={18} />
            {loading ? t.analyzing : t.fetchAndAnalyze}
          </button>
        </div>
      </div>

      {/* Weather Forecast Strip */}
      {forecast && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-main)' }}>
              {t.weatherOverview} ({activeLocation})
            </h3>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>
              {forecast.source} • {forecast.period}
            </span>
          </div>

          <div className="forecast-strip">
            {forecast.daily_forecasts.map((d) => (
              <WeatherCard key={d.date} day={d} />
            ))}
          </div>
        </div>
      )}

      {/* Risk Results Breakdown */}
      {riskResult && (
        <div className="card" style={{ borderLeft: `6px solid ${riskResult.overall_risk === 'High' ? '#DC2626' : riskResult.overall_risk === 'Medium' ? '#D97706' : '#166534'}` }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
            <div>
              <span style={{ fontSize: '0.85rem', color: '#64748B' }}>
                {t.overallRiskLevel} for {activeLocation}
              </span>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '0.25rem' }}>
                <span style={{ fontSize: '1.5rem', fontWeight: 700, color: '#1F2937' }}>
                  {riskResult.crop} • {lang === 'ta' ? PADDY_STAGES.find((s) => s.id === stage)?.ta : stage}
                </span>
                <RiskBadge level={riskResult.overall_risk} t={t} />
              </div>
            </div>

            {/* Trigger Alert Button */}
            <button
              className="btn btn-primary"
              onClick={() =>
                onOpenAlertModal({
                  hazard: riskResult.hazards[0]?.hazard || 'Heavy Rainfall',
                  riskLevel: riskResult.overall_risk,
                  triggerValue: riskResult.hazards[0]?.trigger_value || '',
                })
              }
            >
              <Send size={16} />
              {t.triggerWarningAlert} ({matchingFarmers.length} registered in area)
            </button>
          </div>

          {/* Language Intelligence Narrative Advisory Banner */}
          {warningReport && (
            <div
              style={{
                background: '#E8F3E8',
                border: '1px solid #A7F3D0',
                borderRadius: 'var(--radius-sm)',
                padding: '1.1rem 1.35rem',
                marginBottom: '1.5rem',
              }}
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  marginBottom: '0.4rem',
                  color: '#166534',
                  fontWeight: 700,
                  fontSize: '0.9rem',
                }}
              >
                <Languages size={18} color="#166534" />
                <span>
                  {lang === 'ta'
                    ? 'தமிழ் அக்ரி AI வேளாண் ஆலோசனை (Language Intelligence)'
                    : 'TamilAgri AI Climate Advisory (Language Intelligence)'}
                </span>
              </div>
              <p style={{ fontSize: '1rem', color: '#1F2937', lineHeight: 1.6, fontWeight: 500 }}>
                {warningReport.warning_text}
              </p>
            </div>
          )}

          {/* Hazard Cards Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.25rem' }}>
            {riskResult.hazards.map((hazardItem) => (
              <div
                key={hazardItem.hazard}
                style={{
                  background: '#F8FAFC',
                  border: '1px solid #E2E8F0',
                  borderRadius: 'var(--radius-sm)',
                  padding: '1.25rem',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <div style={{ fontWeight: 700, fontSize: '1.1rem', color: '#1F2937' }}>
                    {lang === 'ta' && hazardItem.hazard === 'Heavy Rainfall'
                      ? 'கனமழை இடர்பாடு'
                      : lang === 'ta' && hazardItem.hazard === 'Extreme Heat'
                      ? 'கடும் வெப்ப இடர்பாடு'
                      : hazardItem.hazard}
                  </div>
                  <RiskBadge level={hazardItem.risk_level} t={t} />
                </div>

                <div style={{ fontSize: '0.8rem', color: '#64748B', marginBottom: '0.75rem', fontFamily: 'monospace' }}>
                  {hazardItem.trigger_value} | Threshold: {hazardItem.threshold_info}
                </div>

                <div style={{ marginBottom: '1rem' }}>
                  <div style={{ fontSize: '0.8rem', fontWeight: 600, color: '#475569', marginBottom: '0.25rem' }}>
                    {lang === 'ta' ? 'காரணம் (Reason):' : 'Risk Explanation:'}
                  </div>
                  <p style={{ fontSize: '0.9rem', color: '#1F2937', lineHeight: 1.5 }}>
                    {lang === 'ta' ? hazardItem.reason_ta : hazardItem.reason_en}
                  </p>
                </div>

                <div
                  style={{
                    background: '#E8F3E8',
                    borderLeft: '4px solid #166534',
                    padding: '0.85rem 1rem',
                    borderRadius: '0 6px 6px 0',
                  }}
                >
                  <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#166534', marginBottom: '0.25rem' }}>
                    {lang === 'ta' ? 'பரிந்துரைக்கப்படும் முன்னெச்சரிக்கை (Precaution):' : 'Precautionary Guidance:'}
                  </div>
                  <p style={{ fontSize: '0.88rem', color: '#1F2937', lineHeight: 1.5 }}>
                    {lang === 'ta' ? hazardItem.precaution_ta : hazardItem.precaution_en}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
