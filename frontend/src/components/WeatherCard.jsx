import React from 'react';
import { CloudRain, Sun, Cloud, Thermometer } from 'lucide-react';

export default function WeatherCard({ day }) {
  const isRainy = day.rainfall_mm > 5.0;
  const isHot = day.temp_max_c > 38.0;

  return (
    <div className="forecast-day-card">
      <div className="forecast-date">{day.date}</div>
      <div style={{ margin: '0.4rem 0', color: isHot ? '#D97706' : isRainy ? '#0F766E' : '#166534' }}>
        {isRainy ? <CloudRain size={24} /> : isHot ? <Sun size={24} /> : <Cloud size={24} />}
      </div>
      <div className="forecast-temp">
        {Math.round(day.temp_max_c)}° / {Math.round(day.temp_min_c)}°C
      </div>
      <div className="forecast-rain">
        <CloudRain size={12} />
        <span>{day.rainfall_mm} mm</span>
      </div>
      <div className="forecast-cond">{day.weather_condition}</div>
    </div>
  );
}
