import React, { useState, useEffect } from 'react';
import { UserPlus, Users, Trash2, Send, CheckCircle2, AlertCircle } from 'lucide-react';
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
  'Villupuram',
];

const STAGES = ['Nursery', 'Tillering', 'Flowering', 'Grain filling', 'Harvest'];

export default function FarmerRegistration({ t, lang, onOpenAlertModal, onFarmerUpdated }) {
  const [farmers, setFarmers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Form state
  const [name, setName] = useState('');
  const [mobile, setMobile] = useState('');
  const [location, setLocation] = useState('Thanjavur');
  const [customLoc, setCustomLoc] = useState('');
  const [crop, setCrop] = useState('Paddy');
  const [growthStage, setGrowthStage] = useState('Flowering');
  const [preferredLanguage, setPreferredLanguage] = useState(lang || 'ta');

  const fetchFarmers = async () => {
    setLoading(true);
    try {
      const data = await api.getFarmers();
      setFarmers(data);
      if (onFarmerUpdated) onFarmerUpdated(data);
    } catch (err) {
      setError('Could not load farmers list.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFarmers();
  }, []);

  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    const finalLocation = customLoc.trim() || location;

    // Validate phone number client-side before sending
    const cleanedPhone = mobile.replace(/[\s\-\(\)]/g, '');
    if (!/^[6-9]\d{9}$/.test(cleanedPhone) && !/^\+91[6-9]\d{9}$/.test(cleanedPhone)) {
      setError(t.phoneValidationHelp);
      return;
    }

    setSubmitting(true);
    try {
      await api.createFarmer({
        name: name.trim(),
        mobile_number: cleanedPhone,
        location: finalLocation,
        crop,
        growth_stage: growthStage,
        preferred_language: preferredLanguage,
      });

      setSuccess(`Farmer '${name.trim()}' successfully registered!`);
      setName('');
      setMobile('');
      setCustomLoc('');
      await fetchFarmers();
    } catch (err) {
      setError(err.message || 'Registration failed');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(t.deleteConfirm)) return;
    try {
      await api.deleteFarmer(id);
      await fetchFarmers();
    } catch (err) {
      setError(err.message || 'Failed to remove farmer profile');
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '1.5rem' }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.25rem' }}>
          {t.regTitle}
        </h1>
        <p style={{ color: 'var(--text-dim)', fontSize: '0.95rem' }}>{t.regSubtitle}</p>
      </div>

      <div className="grid-2col">
        {/* Form Card */}
        <div className="card">
          <h2 className="card-title">
            <UserPlus size={20} color="var(--primary-400)" />
            {t.regTitle}
          </h2>

          {error && (
            <div style={{ padding: '0.75rem 1rem', background: 'rgba(239, 68, 68, 0.2)', border: '1px solid #ef4444', borderRadius: '8px', color: '#fca5a5', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.9rem' }}>
              <AlertCircle size={16} /> {error}
            </div>
          )}

          {success && (
            <div style={{ padding: '0.75rem 1rem', background: 'rgba(16, 185, 129, 0.2)', border: '1px solid #10b981', borderRadius: '8px', color: '#6ee7b7', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.9rem' }}>
              <CheckCircle2 size={16} /> {success}
            </div>
          )}

          <form onSubmit={handleRegister}>
            <div className="form-group">
              <label className="form-label">{t.farmerName} *</label>
              <input
                type="text"
                className="form-input"
                required
                placeholder="e.g., K. Selvakumar / கே. செல்வக்குமார்"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">{t.mobileNumber} *</label>
              <input
                type="tel"
                className="form-input"
                required
                placeholder="9876543210"
                value={mobile}
                onChange={(e) => setMobile(e.target.value)}
              />
              <div className="form-help">{t.phoneValidationHelp}</div>
            </div>

            <div className="form-group">
              <label className="form-label">{t.locationDistrict} *</label>
              <select
                className="form-select"
                style={{ marginBottom: '0.5rem' }}
                value={location}
                onChange={(e) => {
                  setLocation(e.target.value);
                  setCustomLoc('');
                }}
              >
                {TN_DISTRICTS.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
              <input
                type="text"
                className="form-input"
                placeholder="Or specify village/taluk (e.g. Kumbakonam, Thanjavur)"
                value={customLoc}
                onChange={(e) => setCustomLoc(e.target.value)}
              />
            </div>

            <div className="grid-2col" style={{ gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <label className="form-label">{t.cropType}</label>
                <select className="form-select" value={crop} onChange={(e) => setCrop(e.target.value)}>
                  <option value="Paddy">{t.paddyCrop}</option>
                </select>
              </div>

              <div>
                <label className="form-label">{t.growthStage}</label>
                <select
                  className="form-select"
                  value={growthStage}
                  onChange={(e) => setGrowthStage(e.target.value)}
                >
                  {STAGES.map((s) => (
                    <option key={s} value={s}>
                      {s}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">{t.prefLang} *</label>
              <div style={{ display: 'flex', gap: '1rem' }}>
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', cursor: 'pointer', color: 'var(--text-main)', fontSize: '0.9rem' }}>
                  <input
                    type="radio"
                    name="prefLang"
                    value="ta"
                    checked={preferredLanguage === 'ta'}
                    onChange={() => setPreferredLanguage('ta')}
                    style={{ accentColor: 'var(--primary-500)' }}
                  />
                  தமிழ் (Tamil SMS)
                </label>
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', cursor: 'pointer', color: 'var(--text-main)', fontSize: '0.9rem' }}>
                  <input
                    type="radio"
                    name="prefLang"
                    value="en"
                    checked={preferredLanguage === 'en'}
                    onChange={() => setPreferredLanguage('en')}
                    style={{ accentColor: 'var(--primary-500)' }}
                  />
                  English SMS
                </label>
              </div>
            </div>

            <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '0.5rem' }} disabled={submitting}>
              <UserPlus size={18} />
              {submitting ? t.registering : t.registerBtn}
            </button>
          </form>
        </div>

        {/* Directory List Card */}
        <div className="card">
          <h2 className="card-title">
            <Users size={20} color="var(--primary-400)" />
            {t.farmerListTitle} ({farmers.length})
          </h2>

          {loading ? (
            <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-dim)' }}>Loading...</div>
          ) : farmers.length === 0 ? (
            <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-dim)' }}>{t.noFarmersYet}</div>
          ) : (
            <div className="table-responsive" style={{ maxHeight: '520px', overflowY: 'auto' }}>
              <table className="table">
                <thead>
                  <tr>
                    <th>{t.farmerName}</th>
                    <th>{t.locationDistrict}</th>
                    <th>{t.growthStage}</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {farmers.map((farmer) => (
                    <tr key={farmer.id}>
                      <td>
                        <div style={{ fontWeight: 600 }}>{farmer.name}</div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', fontFamily: 'monospace' }}>
                          {farmer.mobile_number} • {farmer.preferred_language === 'ta' ? 'தமிழ்' : 'EN'}
                        </div>
                      </td>
                      <td>{farmer.location}</td>
                      <td>
                        <span style={{ color: 'var(--primary-400)', fontSize: '0.85rem' }}>{farmer.growth_stage}</span>
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                          <button
                            className="btn btn-outline btn-sm"
                            title="Dispatch SMS early warning"
                            onClick={() =>
                              onOpenAlertModal({
                                initialFarmerId: farmer.id,
                                hazard: 'Heavy Rainfall',
                                riskLevel: 'High',
                              })
                            }
                          >
                            <Send size={13} />
                          </button>
                          <button
                            className="btn btn-danger btn-sm"
                            title="Delete profile"
                            onClick={() => handleDelete(farmer.id)}
                          >
                            <Trash2 size={13} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
