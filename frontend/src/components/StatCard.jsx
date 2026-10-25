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
          <span
            style={{
              fontSize: '0.72rem',
              fontWeight: 600,
              color: '#166534',
              background: '#E8F3E8',
              padding: '0.15rem 0.5rem',
              borderRadius: '9999px',
              marginTop: '0.35rem',
              display: 'inline-block',
            }}
          >
            {badgeText}
          </span>
        )}
      </div>
    </div>
  );
}
