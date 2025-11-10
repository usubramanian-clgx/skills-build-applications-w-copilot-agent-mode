import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME;
    const apiUrl = codespace 
      ? `https://${codespace}-8000.app.github.dev/api/activities/`
      : 'http://localhost:8000/api/activities/';
    
    console.log('Fetching activities from:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Activities data received:', data);
        // Handle both paginated and plain array responses
        const activitiesData = data.results || data;
        setActivities(Array.isArray(activitiesData) ? activitiesData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching activities:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center mt-5"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="alert alert-danger m-3">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <h2>Activity Log</h2>
      <p className="text-muted">Recent fitness activities from all users</p>
      <table className="table table-striped table-hover">
        <thead className="table-dark">
          <tr>
            <th>Activity Type</th>
            <th>Duration (min)</th>
            <th>Distance</th>
            <th>Calories</th>
            <th>Points</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {activities.slice(0, 20).map(activity => (
            <tr key={activity.id}>
              <td><strong>{activity.activity_type}</strong></td>
              <td>{activity.duration}</td>
              <td>{activity.distance ? `${activity.distance} km` : '-'}</td>
              <td>{activity.calories || '-'}</td>
              <td><span className="badge bg-info">{activity.points}</span></td>
              <td><small>{new Date(activity.date).toLocaleDateString()}</small></td>
            </tr>
          ))}
        </tbody>
      </table>
      {activities.length === 0 && (
        <div className="alert alert-info">No activities found</div>
      )}
      {activities.length > 20 && (
        <p className="text-muted text-center">Showing 20 of {activities.length} activities</p>
      )}
    </div>
  );
}

export default Activities;
