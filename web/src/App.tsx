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
      const response = await fetch('http://localhost:8000/generate-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ feature_spec: featureSpec })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Full response:', data);

      const messages: AgentMessage[] = [];
      const events: TimelineEvent[] = [];

      // Get architecture data
      const archData = data.architecture || data.architecture_design;
      if (archData) {
        messages.push({
          agent_name: archData.agent_name || '🏗️ Architecture Agent',
          role: archData.role || 'Designing system architecture',
          thinking: archData.thinking || 'Analyzing architecture...',
          output: archData.output,
          timestamp: new Date().toLocaleTimeString()
        });

        events.push({
          agent_name: '🏗️ Architecture Agent',
          status: 'completed',
          timestamp: new Date().toLocaleTimeString(),
          duration: 2
        });
      }

      // Get code data - handle multiple possible keys
      let codeData = data.code || data.code_generation || data.generated_code;
      
      if (codeData) {
        console.log('Code data found:', codeData);
        
        messages.push({
          agent_name: codeData.agent_name || '💻 Code Generation Agent',
          role: codeData.role || 'Writing production-ready code',
          thinking: codeData.thinking || 'Generated code...',
          output: codeData.output,
          timestamp: new Date().toLocaleTimeString()
        });

        // Extract code - try multiple fields
        let code = codeData.extracted_code || codeData.code || codeData.output || '';
        
        if (code) {
          console.log('Setting code, length:', code.length);
          setGeneratedCode(code);
        }

        events.push({
          agent_name: '💻 Code Generation Agent',
          status: 'completed',
          timestamp: new Date().toLocaleTimeString(),
          duration: 3
        });
      } else {
        console.warn('No code data found in response');
      }

      setAgentMessages(messages);
      setTimelineEvents(events);
      
    } catch (error) {
      console.error('Error:', error);
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