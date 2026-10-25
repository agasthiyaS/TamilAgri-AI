import React from 'react';
import { AlertTriangle, CheckCircle2, AlertOctagon } from 'lucide-react';

export default function RiskBadge({ level = 'Low', t, showIcon = true }) {
  const norm = level.toLowerCase();
  
  let label = level;
  if (t) {
    if (norm === 'high') label = t.riskHigh;
    else if (norm === 'medium') label = t.riskMedium;
    else label = t.riskLow;
  }

  return (
    <span className={`badge-risk ${norm}`}>
      {showIcon && (
        <>
          {norm === 'high' && <AlertOctagon size={14} />}
          {norm === 'medium' && <AlertTriangle size={14} />}
          {norm === 'low' && <CheckCircle2 size={14} />}
        </>
      )}
      <span>{label}</span>
    </span>
  );
}
