import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserDashboard = () => {
  const [userInfo, setUserInfo] = useState(null);

  // Fetch user data from your API
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/profile') // Update with correct API URL
      .then(response => {
        setUserInfo(response.data);
      })
      .catch(error => console.error('Error fetching user data:', error));
  }, []);

  return (
    <div>
      <h2>User Dashboard</h2>
      {userInfo ? (
        <div>
          <h3>{userInfo.name}</h3>
          <p>Email: {userInfo.email}</p>
          <p>Phone: {userInfo.phone}</p>
          <p>Location: {userInfo.location}</p>
          <div>
            <h4>Your Help Requests</h4>
            <ul>
              {userInfo.requests && userInfo.requests.map((request) => (
                <li key={request.id}>{request.title}</li>
              ))}
            </ul>
          </div>
        </div>
      ) : (
        <p>Loading user data...</p>
      )}
    </div>
  );
};

export default UserDashboard;
