import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import DiscoverForm from './components/DiscoverForm';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [description, setDescription] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [latency, setLatency] = useState(null);
  const [matchedBy, setMatchedBy] = useState(null);

  const handleDiscover = async () => {
    if (!description.trim()) {
      setError('Please enter a product description');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post('http://localhost:8000/api/discover', {
        description: description
      });

      setResults(response.data.recommendations);
      setLatency(response.data.latency_seconds);
      setMatchedBy(response.data.matched_by);
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        'Failed to fetch recommendations. Make sure the backend is running.'
      );
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setDescription('');
    setResults(null);
    setError(null);
    setLatency(null);
    setMatchedBy(null);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1>🏗️ BIS Standard Discovery</h1>
          <p>AI-Powered Recommendation Engine for Indian Building Material Standards</p>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          <div className="form-section">
            <DiscoverForm
              description={description}
              setDescription={setDescription}
              onDiscover={handleDiscover}
              onClear={handleClear}
              loading={loading}
            />
          </div>

          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}

          {loading && <LoadingSpinner />}

          {results && !loading && (
            <ResultsDisplay
              recommendations={results}
              latency={latency}
              matchedBy={matchedBy}
            />
          )}

          {!results && !loading && !error && (
            <div className="empty-state">
              <p>👈 Enter a product description to discover applicable BIS standards</p>
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>Developed for the MSE Compliance Hackathon • Source: BIS SP 21</p>
      </footer>
    </div>
  );
}

export default App;
