
import React, { useState } from 'react';
import { InputSpec } from './components/InputSpec';
import { AgentReasoning } from './components/AgentReasoning';
import { CodeOutput } from './components/CodeOutput';
import { Timeline } from './components/Timeline';
import './App.css';

interface AgentMessage {
  agent_name: string;
  role: string;
  thinking: string;
  output?: string;
  timestamp?: string;
}

interface TimelineEvent {
  agent_name: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  timestamp: string;
  duration?: number;
}

function App() {
  const [spec, setSpec] = useState('');
  const [loading, setLoading] = useState(false);
  const [agentMessages, setAgentMessages] = useState<AgentMessage[]>([]);
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>([]);
  const [generatedCode, setGeneratedCode] = useState('');
  const [generatedTests, setGeneratedTests] = useState('');
  const [securityAudit, setSecurityAudit] = useState('');
  const [currentAgent, setCurrentAgent] = useState('');

  const handleGenerate = async (featureSpec: string) => {
    setSpec(featureSpec);
    setLoading(true);
    setAgentMessages([]);
    setTimelineEvents([]);
    setGeneratedCode('');
    setGeneratedTests('');
    setSecurityAudit('');

    try {
      // TODO: Connect to backend /generate endpoint
      console.log('Generating code for:', featureSpec);
      
      // Placeholder: Show mock data for now
      setAgentMessages([
        {
          agent_name: '🏗️ Architecture Agent',
          role: 'Designing system architecture',
          thinking: 'Analyzing the feature spec... I should design a REST API with FastAPI.',
          timestamp: new Date().toLocaleTimeString()
        }
      ]);
    } catch (error) {
      console.error('Error generating code:', error);
    }

    setLoading(false);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🚀 Multi-Agent Code Generator</h1>
        <p>AI agents collaborate to generate production-ready code</p>
      </header>

      <main className="app-main">
        <div className="container">
          {/* Left column */}
          <div className="left-column">
            <InputSpec onSubmit={handleGenerate} loading={loading} />
            <Timeline events={timelineEvents} currentAgent={currentAgent} />
          </div>

          {/* Right column */}
          <div className="right-column">
            <AgentReasoning messages={agentMessages} isLoading={loading} />
            <CodeOutput
              code={generatedCode}
              tests={generatedTests}
              securityAudit={securityAudit}
              loading={loading}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;