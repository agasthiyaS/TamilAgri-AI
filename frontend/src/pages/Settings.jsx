import React, { useState, useEffect } from 'react';
import { Settings as SettingsIcon, CheckCircle2, ShieldAlert, ExternalLink, Cpu, Database, Radio, BookOpen } from 'lucide-react';
import { api } from '../api';

export default function Settings({ t, lang, setLang, isDemo }) {
  const [settingsData, setSettingsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getSettings()
      .then(setSettingsData)
      .catch((err) => console.error('Failed to load settings:', err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div style={{ marginBottom: '1.5rem' }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.25rem' }}>
          {t.settingsTitle}
        </h1>
        <p style={{ color: 'var(--text-dim)', fontSize: '0.95rem' }}>{t.settingsSubtitle}</p>
      </div>

      <div className="grid-2col" style={{ marginBottom: '2rem' }}>
        {/* System & Adapter Status Card */}
        <div className="card">
          <h2 className="card-title">
            <Cpu size={20} color="#166534" />
            {t.systemHealth}
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '0.75rem', borderBottom: '1px solid #E2E8F0' }}>
              <div>
                <div style={{ fontWeight: 600, color: '#1F2937' }}>Operating Mode</div>
                <div style={{ fontSize: '0.8rem', color: '#64748B' }}>Zero-cost simulation environment</div>
              </div>
              <span className={isDemo ? 'demo-pill' : 'live-pill'}>
                {isDemo ? t.demoMode : t.liveMode}
              </span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '0.75rem', borderBottom: '1px solid #E2E8F0' }}>
              <div>
                <div style={{ fontWeight: 600, color: '#1F2937' }}>{t.weatherProvider}</div>
                <div style={{ fontSize: '0.8rem', color: '#64748B' }}>Active adapter: <code>{settingsData?.weather_provider || 'demo'}</code></div>
              </div>
              <span style={{ fontSize: '0.85rem', color: '#166534', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <CheckCircle2 size={16} color="#166534" /> Ready
              </span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '0.75rem', borderBottom: '1px solid #E2E8F0' }}>
              <div>
                <div style={{ fontWeight: 600, color: '#1F2937' }}>{t.smsProvider}</div>
                <div style={{ fontSize: '0.8rem', color: '#64748B' }}>Active adapter: <code>{settingsData?.sms_provider || 'demo'}</code> (Simulated)</div>
              </div>
              <span style={{ fontSize: '0.85rem', color: '#92400E', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <CheckCircle2 size={16} color="#D97706" /> Simulated
              </span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontWeight: 600, color: '#1F2937' }}>Database Storage</div>
                <div style={{ fontSize: '0.8rem', color: '#64748B' }}>SQLite (Local file <code>tamilagri.db</code>)</div>
              </div>
              <span style={{ fontSize: '0.85rem', color: '#0F766E', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <Database size={16} color="#0F766E" /> Connected
              </span>
            </div>
          </div>
        </div>

        {/* Demo Mode Details & Language Settings */}
        <div className="card">
          <h2 className="card-title">
            <Radio size={20} color="#166534" />
            {t.demoExplanation}
          </h2>

          <p style={{ fontSize: '0.9rem', color: '#64748B', lineHeight: 1.6, marginBottom: '1.25rem' }}>
            {t.demoExplanationText}
          </p>

          <div style={{ background: '#F8FAFC', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid #E2E8F0', marginBottom: '1.25rem' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#1F2937', marginBottom: '0.5rem' }}>
              Dashboard Display Language / மொழி
            </div>
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <button
                className={`btn btn-sm ${lang === 'ta' ? 'btn-primary' : 'btn-outline'}`}
                onClick={() => setLang('ta')}
              >
                தமிழ் (Tamil)
              </button>
              <button
                className={`btn btn-sm ${lang === 'en' ? 'btn-primary' : 'btn-outline'}`}
                onClick={() => setLang('en')}
              >
                English
              </button>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <a
              href="http://127.0.0.1:8000/docs"
              target="_blank"
              rel="noreferrer"
              className="btn btn-outline btn-sm"
              style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}
            >
              <BookOpen size={14} />
              {t.openSwagger}
              <ExternalLink size={12} />
            </a>
          </div>
        </div>
      </div>

      {/* TNAU Verification & Agronomic Thresholds Notice */}
      <div className="card" style={{ borderLeft: '4px solid #D97706' }}>
        <h2 className="card-title" style={{ color: '#92400E' }}>
          <ShieldAlert size={20} color="#D97706" />
          {t.tnauVerificationHeader}
        </h2>
        <p style={{ fontSize: '0.9rem', color: '#64748B', lineHeight: 1.6, marginBottom: '1rem' }}>
          {t.tnauVerificationText}
        </p>
        <div style={{ fontSize: '0.82rem', color: '#475569', background: '#F8FAFC', padding: '0.85rem 1rem', borderRadius: 'var(--radius-sm)', border: '1px solid #E2E8F0' }}>
          <strong style={{ color: '#166534' }}>Configured Rule Thresholds (backend/app/rules/crop_rules.py):</strong>
          <ul style={{ marginLeft: '1.25rem', marginTop: '0.5rem', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
            <li><strong>Nursery:</strong> Heavy Rain &gt; 50mm/day (submergence risk) | Heat &gt; 38°C (seedling scorch)</li>
            <li><strong>Tillering:</strong> Heavy Rain &gt; 65mm/day (tiller inhibition) | Heat &gt; 39°C (transpiration stress)</li>
            <li><strong>Flowering:</strong> Heavy Rain &gt; 40mm/day (pollen wash) | Heat &gt; 36°C (spikelet sterility)</li>
            <li><strong>Grain filling:</strong> Heavy Rain &gt; 50mm/day (crop lodging) | Heat &gt; 38°C (forced maturity & chalkiness)</li>
            <li><strong>Harvest:</strong> Rain &gt; 15mm/day (grain sprouting & machinery stall) | Heat &gt; 40°C (grain sun-cracking)</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
