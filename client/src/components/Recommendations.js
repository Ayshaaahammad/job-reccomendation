import from 'react';
import JobCard from './JobCard';

function Recommendations({ recommendations }) {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Recommended Jobs</h2>
      {recommendations.length === 0 ? (
        <p className="text-gray-500">No recommendations yet. Fill out your profile to get started!</p>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {recommendations.map((job, index) => (
            <JobCard key={index} job={job} />
          ))}
        </div>
      )}
    </div>
  );
}

export default Recommendations;