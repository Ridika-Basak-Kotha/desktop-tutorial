import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const NewRequest = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('');
  const [location, setLocation] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Send a POST request to the backend API to create a new request
      await axios.post('http://127.0.0.1:5000/requests', {
        title,
        description,
        category,
        location,
      });
      
      // Navigate to the home page or another page after successful request submission
      navigate('/');
    } catch (error) {
      console.error('Error creating request:', error);
    }
  };

  return (
    <div>
      <h2>Create a New Request</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title</label>
          <input 
            type="text" 
            value={title} 
            onChange={(e) => setTitle(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Description</label>
          <textarea 
            value={description} 
            onChange={(e) => setDescription(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Category (Optional)</label>
          <input 
            type="text" 
            value={category} 
            onChange={(e) => setCategory(e.target.value)} 
          />
        </div>
        <div>
          <label>Location</label>
          <input 
            type="text" 
            value={location} 
            onChange={(e) => setLocation(e.target.value)} 
            required 
          />
        </div>
        <button type="submit">Submit Request</button>
      </form>
    </div>
  );
};

export default NewRequest;
