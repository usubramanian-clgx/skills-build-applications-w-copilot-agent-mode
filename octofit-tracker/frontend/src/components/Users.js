import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME;
    const apiUrl = codespace 
      ? `https://${codespace}-8000.app.github.dev/api/users/`
      : 'http://localhost:8000/api/users/';
    
    console.log('Fetching users from:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Users data received:', data);
        // Handle both paginated and plain array responses
        const usersData = data.results || data;
        setUsers(Array.isArray(usersData) ? usersData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching users:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center mt-5"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="alert alert-danger m-3">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <h2>OctoFit Users</h2>
      <p className="text-muted">Fitness heroes tracking their progress</p>
      <table className="table table-striped table-hover">
        <thead className="table-dark">
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Points</th>
            <th>Team ID</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td><span className="badge bg-primary">{user.points}</span></td>
              <td><small className="text-muted">{user.team_id}</small></td>
            </tr>
          ))}
        </tbody>
      </table>
      {users.length === 0 && (
        <div className="alert alert-info">No users found</div>
      )}
    </div>
  );
}

export default Users;
