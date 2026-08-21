import React from 'react';
import './Timeline.css';

interface TimelineEvent {
  agent_name: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  timestamp: string;
  duration?: number; // in seconds
}

interface TimelineProps {
  events: TimelineEvent[];
  currentAgent?: string;
}

export const Timeline: React.FC<TimelineProps> = ({ events, currentAgent }) => {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return '✅';
      case 'running':
        return '⏳';
      case 'error':
        return '❌';
      case 'pending':
        return '⭕';
      default:
        return '❓';
    }
  };

  const getStatusClass = (status: string) => {
    return `status-${status}`;
  };

  return (
    <div className="timeline">
      <h2>📅 Execution Timeline</h2>

      {events.length === 0 ? (
        <p className="empty-state">No agents have run yet.</p>
      ) : (
        <div className="timeline-container">
          {events.map((event, idx) => (
            <div
              key={idx}
              className={`timeline-item ${getStatusClass(event.status)} ${
                currentAgent === event.agent_name ? 'active' : ''
              }`}
            >
              {/* Timeline dot */}
              <div className="timeline-dot">
                <span className="status-icon">{getStatusIcon(event.status)}</span>
              </div>

              {/* Timeline content */}
              <div className="timeline-content">
                <div className="timeline-header">
                  <h3>{event.agent_name}</h3>
                  <span className={`status-badge ${getStatusClass(event.status)}`}>
                    {event.status.toUpperCase()}
                  </span>
                </div>

                <div className="timeline-meta">
                  <span className="timestamp">⏰ {event.timestamp}</span>
                  {event.duration && (
                    <span className="duration">⏱️ {event.duration}s</span>
                  )}
                </div>
              </div>

              {/* Connecting line */}
              {idx < events.length - 1 && <div className="timeline-line"></div>}
            </div>
          ))}
        </div>
      )}

      {currentAgent && (
        <div className="current-agent-indicator">
          <p>🔄 Currently running: <strong>{currentAgent}</strong></p>
        </div>
      )}
    </div>
  );
};