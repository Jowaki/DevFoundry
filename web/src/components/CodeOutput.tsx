import React, { useState } from 'react';
import './CodeOutput.css';

interface CodeOutputProps {
  code?: string;
  tests?: string;
  securityAudit?: string;
  loading: boolean;
}

export const CodeOutput: React.FC<CodeOutputProps> = ({
  code,
  tests,
  securityAudit,
  loading
}) => {
  const [activeTab, setActiveTab] = useState<'code' | 'tests' | 'security'>('code');

  const downloadFile = (content: string, filename: string) => {
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const handleDownloadCode = () => {
    if (code) downloadFile(code, 'generated_code.py');
  };

  const handleDownloadTests = () => {
    if (tests) downloadFile(tests, 'generated_tests.py');
  };

  return (
    <div className="code-output">
      <div className="code-header">
        <h2>📝 Generated Code</h2>
        <button 
          className="download-btn" 
          onClick={handleDownloadCode}
          disabled={!code || loading}
        >
          ⬇️ Download Code
        </button>
      </div>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'code' ? 'active' : ''}`}
          onClick={() => setActiveTab('code')}
        >
          Python Code
        </button>
        <button
          className={`tab ${activeTab === 'tests' ? 'active' : ''}`}
          onClick={() => setActiveTab('tests')}
          disabled={!tests}
        >
          Tests
        </button>
        <button
          className={`tab ${activeTab === 'security' ? 'active' : ''}`}
          onClick={() => setActiveTab('security')}
          disabled={!securityAudit}
        >
          Security Audit
        </button>
      </div>

      <div className="code-container">
        {loading ? (
          <p className="loading-text">Generating code...</p>
        ) : !code && !tests && !securityAudit ? (
          <p className="empty-state">No code generated yet. Submit a spec above!</p>
        ) : (
          <>
            {activeTab === 'code' && code && (
              <pre className="code-block">
                <code>{code}</code>
              </pre>
            )}
            {activeTab === 'tests' && tests && (
              <pre className="code-block">
                <code>{tests}</code>
              </pre>
            )}
            {activeTab === 'security' && securityAudit && (
              <pre className="code-block">
                <code>{securityAudit}</code>
              </pre>
            )}
          </>
        )}
      </div>

      {code && (
        <div className="code-stats">
          <span>📊 Lines of code: {code.split('\n').length}</span>
        </div>
      )}
    </div>
  );
};