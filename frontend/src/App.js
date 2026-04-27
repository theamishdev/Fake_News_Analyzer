import React, { useState } from 'react';
import axios from 'axios';
import { Search, AlertCircle, CheckCircle, Newspaper, ArrowRight, Loader2, ShieldAlert } from 'lucide-react';
import './App.css';

function App() {
  const [newsText, setNewsText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeNews = async (e) => {
    e.preventDefault();
    if (!newsText.trim()) return;

    setLoading(true);
    setResult(null);
    setError(null);

    try {
      // The API endpoint should match the one in our backend
      const response = await axios.post('http://localhost:8080/api/news/analyze', {
        text: newsText
      });
      setResult(response.data);
    } catch (err) {
      console.error('Error analyzing news:', err);
      setError(err.response?.data?.error || 'Failed to connect to the analysis service.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <nav className="navbar">
        <div className="nav-content">
          <div className="logo">
            <Newspaper className="logo-icon" />
            <span>Smart News Analyzer</span>
          </div>
          <div className="nav-version">v1.2.0 (Stable)</div>
        </div>
      </nav>

      <main className="main-content">
        <header className="hero">
          <h1>Stop Fake News. <span className="highlight">Instantly.</span></h1>
          <p>Paste any news snippet or headline below to analyze its authenticity using our advanced AI engine.</p>
        </header>

        <section className="analyzer-section">
          <form onSubmit={analyzeNews} className="analyzer-form">
            <div className="input-group">
              <textarea
                value={newsText}
                onChange={(e) => setNewsText(e.target.value)}
                placeholder="Paste news content here..."
                rows={6}
                required
              />
              <button type="submit" disabled={loading || !newsText}>
                {loading ? (
                  <><Loader2 className="spinning" /> Analyzing...</>
                ) : (
                  <><Search /> Analyze Now</>
                )}
              </button>
            </div>
          </form>

          {error && (
            <div className="alert error-alert">
              <ShieldAlert className="alert-icon" />
              <div className="alert-text">
                <strong>Analysis Failed</strong>
                <p>{error}</p>
              </div>
            </div>
          )}

          {result && (
            <div className={`result-card ${result.result.toLowerCase()}`}>
              <div className="result-header">
                {result.result === 'Real' ? (
                  <CheckCircle className="result-icon success" />
                ) : (
                  <AlertCircle className="result-icon warning" />
                )}
                <div className="result-title">
                  <h2>This news is likely <span className="status-text">{result.result}</span></h2>
                  <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
                </div>
              </div>
              <div className="result-body">
                <div className="meter-container">
                  <div 
                    className="meter-fill" 
                    style={{ width: `${result.confidence * 100}%` }}
                  ></div>
                </div>
                <p className="disclaimer">
                  * Analysis based on current model version {result.model_version}. 
                  Always verify important news through multiple reliable sources.
                </p>
              </div>
            </div>
          )}
        </section>

        <section className="features">
          <div className="feature-card">
            <h3>AI Driven</h3>
            <p>Powered by a specialized NLP model for fake news detection.</p>
          </div>
          <div className="feature-card">
            <h3>Fast Response</h3>
            <p>Get results in milliseconds with our optimized microservice architecture.</p>
          </div>
          <div className="feature-card">
            <h3>Secure</h3>
            <p>Your inputs are processed securely and never shared with third parties.</p>
          </div>
        </section>
      </main>

      <footer className="footer">
        <p>&copy; 2026 Smart News Analyzer. Built with React, Spring Boot, and Python.</p>
      </footer>
    </div>
  );
}

export default App;
