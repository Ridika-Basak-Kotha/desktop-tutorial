import React, { useState, useEffect } from 'react';
import axios from 'axios';

const VolunteerDashboard = () => {
  const [volunteerInfo, setVolunteerInfo] = useState(null);

  // Fetch volunteer data from your API
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/volunteerProfile') // Update with correct API URL
      .then(response => {
        setVolunteerInfo(response.data);
      })
      .catch(error => console.error('Error fetching volunteer data:', error));
  }, []);

  return (
    <div>
      <h2>Volunteer Dashboard</h2>
      {volunteerInfo ? (
        <div>
          <h3>{volunteerInfo.name}</h3>
          <p>Email: {volunteerInfo.email}</p>
          <p>Skills: {volunteerInfo.skills.join(', ')}</p>
          <p>Availability: {volunteerInfo.availability}</p>
          <div>
            <h4>Your Responses</h4>
            <ul>
              {volunteerInfo.responses && volunteerInfo.responses.map((response) => (
                <li key={response.id}>
                  {response.request.title} - Status: {response.status}
                </li>
              ))}
            </ul>
          </div>
        </div>
      ) : (
        <p>Loading volunteer data...</p>
      )}
    </div>
  );
};

export default VolunteerDashboard;
