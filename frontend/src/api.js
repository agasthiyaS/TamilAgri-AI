const API_BASE = '/api';

async function handleResponse(response) {
  if (!response.ok) {
    let errorDetail = 'API Request Failed';
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || JSON.stringify(errorJson);
    } catch {
      errorDetail = await response.text();
    }
    throw new Error(errorDetail || `HTTP Error ${response.status}`);
  }
  if (response.status === 204) return null;
  return response.json();
}

export const api = {
  getHealth: () => fetch(`${API_BASE}/health`).then(handleResponse),
  getSettings: () => fetch(`${API_BASE}/settings`).then(handleResponse),
  
  // Farmers
  getFarmers: () => fetch(`${API_BASE}/farmers`).then(handleResponse),
  getFarmer: (id) => fetch(`${API_BASE}/farmers/${id}`).then(handleResponse),
  createFarmer: (data) =>
    fetch(`${API_BASE}/farmers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(handleResponse),
  deleteFarmer: (id) =>
    fetch(`${API_BASE}/farmers/${id}`, { method: 'DELETE' }).then(handleResponse),

  // Weather & Risk
  getForecast: (location) =>
    fetch(`${API_BASE}/weather/forecast?location=${encodeURIComponent(location)}`).then(handleResponse),
  analyzeRisk: (data) =>
    fetch(`${API_BASE}/risk/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(handleResponse),

  // Alerts
  sendAlert: (payload) =>
    fetch(`${API_BASE}/alerts/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }).then(handleResponse),
  getAlertHistory: (params = {}) => {
    const query = new URLSearchParams();
    if (params.hazard) query.append('hazard', params.hazard);
    if (params.risk_level) query.append('risk_level', params.risk_level);
    if (params.status) query.append('status', params.status);
    const qs = query.toString();
    return fetch(`${API_BASE}/alerts/history${qs ? '?' + qs : ''}`).then(handleResponse);
  },
};
