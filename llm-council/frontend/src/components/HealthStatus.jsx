import { useState, useEffect } from 'react';
import './HealthStatus.css';

export default function HealthStatus() {
  const [healthStatus, setHealthStatus] = useState({ models: {}, chairman: '' });
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    // Check health immediately
    checkHealth();

    // Then check every 30 seconds
    const interval = setInterval(checkHealth, 30000);

    return () => clearInterval(interval);
  }, []);

  const checkHealth = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/health');
      const data = await response.json();
      setHealthStatus(data);
    } catch (error) {
      console.error('Failed to check health:', error);
    }
  };

  const onlineCount = Object.values(healthStatus.models).filter(Boolean).length;
  const totalCount = Object.keys(healthStatus.models).length;
  const allOnline = onlineCount === totalCount && totalCount > 0;

  return (
    <div className="health-status">
      <button 
        className="health-status-toggle" 
        onClick={() => setIsExpanded(!isExpanded)}
        title="LLM Health Status"
      >
        <span className={`status-indicator ${allOnline ? 'online' : 'partial'}`}>
          {allOnline ? '●' : '◐'}
        </span>
        <span className="status-text">
          {onlineCount}/{totalCount} Online
        </span>
      </button>

      {isExpanded && (
        <div className="health-status-panel">
          <div className="health-status-header">LLM Status</div>
          <div className="health-status-list">
            {Object.entries(healthStatus.models).map(([model, status]) => {
              const isChairman = model === healthStatus.chairman;
              return (
                <div key={model} className="health-status-item">
                  <span className={`model-status-indicator ${status ? 'online' : 'offline'}`}>
                    ●
                  </span>
                  <span className="model-name">
                    {model}
                    {isChairman && <span className="chairman-badge">Chairman</span>}
                  </span>
                  <span className={`model-status ${status ? 'online' : 'offline'}`}>
                    {status ? 'Online' : 'Offline'}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
