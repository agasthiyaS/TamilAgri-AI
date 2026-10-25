import React from 'react';

export default function StatCard({ title, value, icon: Icon, badgeText, badgeType = 'primary' }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">
        <Icon size={24} />
      </div>
      <div>
        <div className="stat-value">{value}</div>
        <div className="stat-label">{title}</div>
        {badgeText && (
          <span style={{ fontSize: '0.75rem', color: 'var(--primary-400)', marginTop: '0.25rem', display: 'inline-block' }}>
            {badgeText}
          </span>
        )}
      </div>
    </div>
  );
}
