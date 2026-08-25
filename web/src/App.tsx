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

  const handleGenerate = async (featureSpec: string) => {
    setSpec(featureSpec);
    setLoading(true);
    setAgentMessages([]);
    setTimelineEvents([]);
    setGeneratedCode('');
    setGeneratedTests('');
    setSecurityAudit('');

    try {
      console.log('🚀 Starting full pipeline...');
      
      const response = await fetch('http://localhost:8000/generate-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ feature_spec: featureSpec })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('📦 Full pipeline response:', data);

      const messages: AgentMessage[] = [];
      const events: TimelineEvent[] = [];

      // Process each agent's output
      const agentOrder = [
        { key: 'architecture', name: '🏗️ Architecture Agent' },
        { key: 'code', name: '💻 Code Generation Agent' },
        { key: 'tests', name: '🧪 Testing Agent' },
        { key: 'security', name: '🔒 Security Agent' }
      ];

      agentOrder.forEach((agent) => {
        const agentData = data[agent.key];
        if (agentData && !agentData.error) {
          messages.push({
            agent_name: agentData.agent_name || agent.name,
            role: agentData.role || '',
            thinking: agentData.thinking || '',
            output: agentData.output,
            timestamp: new Date().toLocaleTimeString()
          });

          events.push({
            agent_name: agent.name,
            status: 'completed',
            timestamp: new Date().toLocaleTimeString(),
            duration: 2
          });

          // Set content for each agent type
          if (agent.key === 'code') {
            const code = agentData.extracted_code || agentData.output || '';
            setGeneratedCode(code);
            console.log('✅ Code set:', code.length, 'chars');
          } else if (agent.key === 'tests') {
            const tests = agentData.extracted_tests || agentData.output || '';
            setGeneratedTests(tests);
            console.log('✅ Tests set:', tests.length, 'chars');
          } else if (agent.key === 'security') {
            setSecurityAudit(agentData.output || '');
            console.log('✅ Security audit set:', agentData.output?.length || 0, 'chars');
          }
        }
      });

      setAgentMessages(messages);
      setTimelineEvents(events);
      console.log('✅ UI updated with all 4 agents');
      
    } catch (error) {
      console.error('❌ Error:', error);
      const errorMsg = error instanceof Error ? error.message : String(error);
      alert('Error: ' + errorMsg);
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
          <div className="left-column">
            <InputSpec onSubmit={handleGenerate} loading={loading} />
            <Timeline events={timelineEvents} currentAgent="" />
          </div>

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