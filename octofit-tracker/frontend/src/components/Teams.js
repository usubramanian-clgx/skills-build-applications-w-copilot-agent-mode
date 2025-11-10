import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME;
    const apiUrl = codespace 
      ? `https://${codespace}-8000.app.github.dev/api/teams/`
      : 'http://localhost:8000/api/teams/';
    
    console.log('Fetching teams from:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams data received:', data);
        // Handle both paginated and plain array responses
        const teamsData = data.results || data;
        setTeams(Array.isArray(teamsData) ? teamsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching teams:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center mt-5"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="alert alert-danger m-3">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <h2>OctoFit Teams</h2>
      <p className="text-muted">Competing teams in the fitness challenge</p>
      <div className="row">
        {teams.map(team => (
          <div key={team.id} className="col-md-6 mb-4">
            <div className="card">
              <div className="card-header bg-success text-white">
                <h5 className="card-title mb-0">{team.name}</h5>
              </div>
              <div className="card-body">
                <p className="card-text">{team.description}</p>
                <div className="d-flex justify-content-between align-items-center">
                  <span className="text-muted">Total Points</span>
                  <span className="badge bg-success fs-5">{team.total_points}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      {teams.length === 0 && (
        <div className="alert alert-info">No teams found</div>
      )}
    </div>
  );
}

export default Teams;
