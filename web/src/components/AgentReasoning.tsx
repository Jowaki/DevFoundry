import React from 'react';
import './AgentReasoning.css';

interface AgentMessage {
  agent_name: string;
  role: string;
  thinking: string;
  output?: string;
  timestamp?: string;
}

interface AgentReasoningProps {
  messages: AgentMessage[];
  isLoading: boolean;
}

export const AgentReasoning: React.FC<AgentReasoningProps> = ({
  messages,
  isLoading
}) => {
  return (
    <div className="agent-reasoning">
      <h2>🤖 Agent Reasoning</h2>
      
      <div className="messages-container">
        {messages.length === 0 && !isLoading && (
          <p className="empty-state">No agents have run yet. Submit a spec to start!</p>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className="agent-message">
            <div className="agent-header">
              <span className="agent-name">{msg.agent_name}</span>
              <span className="agent-role">{msg.role}</span>
              {msg.timestamp && <span className="timestamp">{msg.timestamp}</span>}
            </div>
            
            <div className="agent-thinking">
              <p><strong>Thinking:</strong></p>
              <p>{msg.thinking}</p>
            </div>

            {msg.output && (
              <div className="agent-output">
                <p><strong>Output:</strong></p>
                <pre>{msg.output}</pre>
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="agent-message loading">
            <div className="agent-header">
              <span className="agent-name">⏳ Processing</span>
            </div>
            <div className="spinner"></div>
            <p>Agents are working...</p>
          </div>
        )}
      </div>
    </div>
  );
};