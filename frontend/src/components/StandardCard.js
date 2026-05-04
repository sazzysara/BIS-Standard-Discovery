import React from 'react';
import './StandardCard.css';

function StandardCard({ standard, rank }) {
  return (
    <div className="standard-card">
      <div className="card-rank">#{rank}</div>
      
      <div className="card-header">
        <h3 className="standard-id">{standard.standard_id}</h3>
      </div>

      <div className="card-body">
        <p className="rationale">{standard.rationale}</p>
      </div>

      <div className="card-footer">
        <span className="badge">📚 Verified Standard</span>
      </div>
    </div>
  );
}

export default StandardCard;
