import React, { useState } from 'react';
import './InputSpec.css';

interface InputSpecProps {
  onSubmit: (spec: string) => void;
  loading?: boolean;
}

export const InputSpec: React.FC<InputSpecProps> = ({ onSubmit, loading = false }) => {
  const [spec, setSpec] = useState('');
  const [characterCount, setCharacterCount] = useState(0);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setSpec(value);
    setCharacterCount(value.length);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (spec.trim()) {
      onSubmit(spec);
      setSpec('');
      setCharacterCount(0);
    }
  };

  const handleClear = () => {
    setSpec('');
    setCharacterCount(0);
  };

  // Example specs for quick testing
  const exampleSpecs = [
    'Build a REST API for a todo app with user authentication',
    'Create a file upload service with virus scanning',
    'Build a real-time chat API with message history',
    'Create an e-commerce cart service with inventory management'
  ];

  const insertExample = (example: string) => {
    setSpec(example);
    setCharacterCount(example.length);
  };

  return (
    <div className="input-spec">
      <h2>📋 Feature Specification</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="spec-input">Describe the code you want to generate:</label>
          <textarea
            id="spec-input"
            value={spec}
            onChange={handleChange}
            placeholder="Example: Build a REST API for a todo app with user authentication, database persistence, and JWT tokens..."
            rows={6}
            disabled={loading}
          />
          <div className="char-count">
            {characterCount} characters
          </div>
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="submit-btn"
            disabled={!spec.trim() || loading}
          >
            {loading ? '⏳ Generating...' : '🚀 Generate Code'}
          </button>
          <button
            type="button"
            className="clear-btn"
            onClick={handleClear}
            disabled={loading}
          >
            Clear
          </button>
        </div>
      </form>

      <div className="examples">
        <h3>📌 Quick Examples:</h3>
        <div className="examples-list">
          {exampleSpecs.map((example, idx) => (
            <button
              key={idx}
              className="example-btn"
              onClick={() => insertExample(example)}
              disabled={loading}
              title="Click to insert this example"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      <div className="info-box">
        <p>💡 <strong>Tip:</strong> Be specific! Include details about features, authentication, database requirements, etc.</p>
      </div>
    </div>
  );
};