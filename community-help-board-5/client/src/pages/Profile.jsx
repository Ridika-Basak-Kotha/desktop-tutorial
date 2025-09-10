import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Profile = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Fetch user profile data from the server 
    axios.get('http://127.0.0.1:5000/profile')
      .then(response => setUser(response.data))
      .catch(error => console.error('Error fetching profile:', error));
  }, []);

  if (!user) {
    return <p>Loading profile...</p>;
  }

  return (
    <div>
      <h2>User Profile</h2>
      <p><strong>Email:</strong> {user.email}</p>
      {/* Display user-specific requests here */}
    </div>
  );
};

export default Profile;
