import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const Home = () => {
  const [requests, setRequests] = useState([]);

  // Fetch new requests from the server (ensure you have an API endpoint)
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/requests') // Update the API URL
      .then(response => {
        setRequests(response.data);
      })
      .catch(error => console.error('Error fetching requests:', error));
  }, []);

  return (
    <div>
      <h1>Welcome to the Community Help Board</h1>
      <div>
        <h2>New Requests</h2>
        {requests.length === 0 ? (
          <p>No new requests at the moment.</p>
        ) : (
          <ul>
            {requests.map(request => (
              <li key={request.id}>
                <Link to={`/request/${request.id}`}>{request.title}</Link>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div>
        <Link to="/login">Login</Link> | <Link to="/register">Register</Link> | <Link to="/profile">Profile</Link>
      </div>
    </div>
  );
};

export default Home;
