import React from 'react';
import './App.css';
import UserProfileForm from './components/UserProfileForm';
import Recommendations from './components/Recommendations';

function App() {
  const [recommendations, setRecommendations] = React.useState([]);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-center">Job Recommendation System</h1>
        <UserProfileForm setRecommendations={setRecommendations} />
        <Recommendations recommendations={recommendations} />
      </div>
    </div>
  );
}

export default App;