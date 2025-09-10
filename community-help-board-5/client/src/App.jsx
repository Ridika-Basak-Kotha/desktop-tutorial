import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import UserDashboard from './pages/Dashboard/UserDashboard';
import VolunteerDashboard from './pages/Dashboard/VolunteerDashboard';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  const isAuthenticated = true; // You can replace this with real authentication logic

  return (
    <Router>
      <div>
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/login" component={Login} />
          <Route path="/register" component={Register} />
          <Route path="/profile" component={Profile} />
          
          {/* Protected Routes */}
          <ProtectedRoute 
            path="/user-dashboard" 
            component={UserDashboard} 
            isAuthenticated={isAuthenticated} 
          />
          <ProtectedRoute 
            path="/volunteer-dashboard" 
            component={VolunteerDashboard} 
            isAuthenticated={isAuthenticated} 
          />
        </Switch>
      </div>
    </Router>
  );
}

export default App;

