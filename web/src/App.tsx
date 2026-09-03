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
  const [regenerating, setRegenerating] = useState(false);
  const [agentMessages, setAgentMessages] = useState<AgentMessage[]>([]);
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>([]);
  const [generatedCode, setGeneratedCode] = useState('');
  const [generatedTests, setGeneratedTests] = useState('');
  const [securityAudit, setSecurityAudit] = useState('');
  const [issues, setIssues] = useState<any>({ critical: [], medium: [] });
  const [fullResult, setFullResult] = useState<any>(null);

  const handleGenerate = async (featureSpec: string) => {
    setSpec(featureSpec);
    setLoading(true);
    setAgentMessages([]);
    setTimelineEvents([]);
    setGeneratedCode('');
    setGeneratedTests('');
    setSecurityAudit('');
    setIssues({ critical: [], medium: [] });

    try {
      console.log('🚀 Starting pipeline...');
      
      const response = await fetch('http://localhost:8000/generate-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ feature_spec: featureSpec })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('📦 Pipeline result:', data);

      const messages: AgentMessage[] = [];
      const events: TimelineEvent[] = [];

      // Process pipeline
      const pipeline = data.pipeline || {};
      
      ['architecture', 'code', 'tests', 'security'].forEach((agent, idx) => {
        const agentData = pipeline[agent];
        if (agentData && !agentData.error) {
          messages.push({
            agent_name: agentData.agent_name,
            role: agentData.role,
            thinking: agentData.thinking,
            output: agentData.output,
            timestamp: new Date().toLocaleTimeString()
          });

          events.push({
            agent_name: agentData.agent_name,
            status: 'completed',
            timestamp: new Date().toLocaleTimeString(),
            duration: idx + 1
          });

          if (agent === 'code') {
            const code = agentData.extracted_code || agentData.output || '';
            setGeneratedCode(code);
          } else if (agent === 'tests') {
            const tests = agentData.extracted_tests || agentData.output || '';
            setGeneratedTests(tests);
          } else if (agent === 'security') {
            setSecurityAudit(agentData.output || '');
          }
        }
      });

      // Set issues
      const extractedIssues = data.issues || { critical: [], medium: [] };
      setIssues(extractedIssues);
      setFullResult(data);

      setAgentMessages(messages);
      setTimelineEvents(events);
      
    } catch (error) {
      console.error('❌ Error:', error);
      alert('Error: ' + error);
    }

    setLoading(false);
  };

  const handleRegenerate = async () => {
    if (!generatedCode || !spec) {
      alert('No code to regenerate');
      return;
    }

    setRegenerating(true);

    try {
      console.log('🔄 Regenerating code with fixes...');
      
      const response = await fetch('http://localhost:8000/regenerate-with-fixes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          feature_spec: spec,
          previous_code: generatedCode,
          issues: issues
        })
      });

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setGeneratedCode(data.regenerated_code || '');
      setSecurityAudit(data.security_audit?.output || '');
      
      alert('✅ Code regenerated with fixes!');
      
    } catch (error) {
      console.error('Error regenerating:', error);
      alert('Error regenerating: ' + error);
    }

    setRegenerating(false);
  };

  const handleDownloadPDF = async () => {
    if (!fullResult) {
      alert('No result to download');
      return;
    }

    try {
      console.log('📄 Generating PDF...');
      
      const response = await fetch('http://localhost:8000/generate-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ result: fullResult })
      });

      if (!response.ok) {
        throw new Error('PDF generation failed');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'code-generation-report.pdf';
      link.click();
      
    } catch (error) {
      console.error('Error downloading PDF:', error);
      alert('Error downloading PDF: ' + error);
    }
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
            
            {/* Action buttons */}
            {generatedCode && (
              <div className="action-buttons">
                <button 
                  onClick={handleRegenerate} 
                  disabled={regenerating || loading}
                  className="btn-regenerate"
                >
                  {regenerating ? '⏳ Regenerating...' : '🔄 Fix Issues & Regenerate'}
                </button>
                <button 
                  onClick={handleDownloadPDF}
                  disabled={loading || regenerating}
                  className="btn-pdf"
                >
                  📄 Download PDF Report
                </button>
              </div>
            )}
          </div>

          <div className="right-column">
            <AgentReasoning messages={agentMessages} isLoading={loading} />
            <CodeOutput
              code={generatedCode}
              tests={generatedTests}
              securityAudit={securityAudit}
              loading={loading}
            />
            
            {/* Issues display */}
            {(issues.critical.length > 0 || issues.medium.length > 0) && (
              <div className="issues-panel">
                <h3>🔍 Issues Found</h3>
                {issues.critical.length > 0 && (
                  <div className="critical">
                    <strong>🔴 Critical ({issues.critical.length})</strong>
                    <ul>
                      {issues.critical.map((issue: string, idx: number) => (
                        <li key={idx}>{issue}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {issues.medium.length > 0 && (
                  <div className="medium">
                    <strong>🟡 Medium ({issues.medium.length})</strong>
                    <ul>
                      {issues.medium.map((issue: string, idx: number) => (
                        <li key={idx}>{issue}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;