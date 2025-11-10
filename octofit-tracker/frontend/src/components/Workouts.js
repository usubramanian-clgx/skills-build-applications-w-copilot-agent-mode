import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME;
    const apiUrl = codespace 
      ? `https://${codespace}-8000.app.github.dev/api/workouts/`
      : 'http://localhost:8000/api/workouts/';
    
    console.log('Fetching workouts from:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts data received:', data);
        // Handle both paginated and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center mt-5"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="alert alert-danger m-3">Error: {error}</div>;

  const getDifficultyBadge = (level) => {
    const badges = {
      'Beginner': 'bg-success',
      'Intermediate': 'bg-info',
      'Advanced': 'bg-warning text-dark',
      'Expert': 'bg-danger'
    };
    return badges[level] || 'bg-secondary';
  };

  return (
    <div className="container mt-4">
      <h2>Personalized Workouts</h2>
      <p className="text-muted">Suggested workout routines for optimal fitness</p>
      <div className="row">
        {workouts.map(workout => (
          <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
            <div className="card h-100">
              <div className="card-header bg-primary text-white">
                <h5 className="card-title mb-0">{workout.workout_name}</h5>
              </div>
              <div className="card-body">
                <p className="card-text">{workout.description}</p>
                <hr />
                <div className="mb-2">
                  <span className="text-muted">Difficulty:</span>
                  <span className={`badge ${getDifficultyBadge(workout.difficulty_level)} ms-2`}>
                    {workout.difficulty_level}
                  </span>
                </div>
                <div className="mb-2">
                  <span className="text-muted">Duration:</span>
                  <strong className="ms-2">{workout.suggested_duration} minutes</strong>
                </div>
                <div className="mb-2">
                  <span className="text-muted">Target Calories:</span>
                  <strong className="ms-2">{workout.target_calories || 'N/A'}</strong>
                </div>
              </div>
              <div className="card-footer">
                <button className="btn btn-primary btn-sm w-100">Start Workout</button>
              </div>
            </div>
          </div>
        ))}
      </div>
      {workouts.length === 0 && (
        <div className="alert alert-info">No workouts found</div>
      )}
    </div>
  );
}

export default Workouts;
