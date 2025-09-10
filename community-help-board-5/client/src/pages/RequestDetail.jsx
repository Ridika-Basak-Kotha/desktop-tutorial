import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const RequestDetail = () => {
  const { id } = useParams();
  const [request, setRequest] = useState(null);

  // Fetch request details based on ID
  useEffect(() => {
    axios.get(`http://127.0.0.1:5000/requests/${id}`)
      .then(response => {
        setRequest(response.data);
      })
      .catch(error => console.error('Error fetching request details:', error));
  }, [id]);

  if (!request) {
    return <p>Loading request details...</p>;
  }

  return (
    <div>
      <h2>{request.title}</h2>
      <p>{request.description}</p>
      <p><strong>Location:</strong> {request.location}</p>
      <p><strong>Requested by:</strong> {request.user}</p>
    </div>
  );
};

export default RequestDetail;
