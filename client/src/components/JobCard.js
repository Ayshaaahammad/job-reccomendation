import React from 'react';

function JobCard({ job }) {
  return (
    <div className="job-card bg-white p-4 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold">{job.title}</h3>
      <p className="text-gray-600">{job.company}</p>
      <p className="text-gray-600">{job.location}</p>
      <p className="text-gray-500 mt-2">{job.description}</p>
      <p className="text-sm text-gray-500 mt-2">Required Skills: {job.skills}</p>
    </div>
  );
}

export default JobCard;