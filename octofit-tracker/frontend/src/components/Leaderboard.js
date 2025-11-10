import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME;
    const apiUrl = codespace 
      ? `https://${codespace}-8000.app.github.dev/api/leaderboard/`
      : 'http://localhost:8000/api/leaderboard/';
    
    console.log('Fetching leaderboard from:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard data received:', data);
        // Handle both paginated and plain array responses
        const leaderboardData = data.results || data;
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center mt-5"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="alert alert-danger m-3">Error: {error}</div>;

  const getRankBadge = (rank) => {
    if (rank === 1) return 'bg-warning text-dark';
    if (rank === 2) return 'bg-secondary';
    if (rank === 3) return 'bg-bronze';
    return 'bg-light text-dark';
  };

  const getRankIcon = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return '';
  };

  return (
    <div className="container mt-4">
      <h2>Fitness Leaderboard</h2>
      <p className="text-muted">Top performers ranked by total points</p>
      <table className="table table-striped table-hover">
        <thead className="table-dark">
          <tr>
            <th style={{width: '80px'}}>Rank</th>
            <th>User</th>
            <th>Team</th>
            <th>Total Points</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map(entry => (
            <tr key={entry.id}>
              <td>
                <span className={`badge ${getRankBadge(entry.rank)} fs-6`}>
                  {getRankIcon(entry.rank)} #{entry.rank}
                </span>
              </td>
              <td><strong>{entry.user_name}</strong></td>
              <td><span className="badge bg-success">{entry.team_name}</span></td>
              <td><span className="badge bg-primary fs-6">{entry.total_points}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
      {leaderboard.length === 0 && (
        <div className="alert alert-info">No leaderboard entries found</div>
      )}
    </div>
  );
}

export default Leaderboard;
