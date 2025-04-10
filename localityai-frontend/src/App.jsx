import React, { useState } from 'react';
import axios from 'axios';

export default function App() {
  const [location, setLocation] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!location) return;
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('http://localhost:5000/generate_summary', {
        location: location,
        vertical: 'general'
      });
      setSummary(response.data.summary);
    } catch (err) {
      setError('Failed to generate summary. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 font-sans">
      <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-xl p-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">LocalityAI Insights</h1>
        <p className="text-gray-600 mb-6">Enter a ZIP code or city to get a personalized summary of local market conditions.</p>

        <div className="flex gap-4 mb-6">
          <input
            type="text"
            className="flex-grow border border-gray-300 rounded-xl px-4 py-2 text-gray-800"
            placeholder="Enter location..."
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
          <button
            onClick={handleGenerate}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-xl"
            disabled={loading}
          >
            {loading ? 'Generating...' : 'Generate'}
          </button>
        </div>

        {error && <div className="text-red-600 mb-4">{error}</div>}

        {summary && (
          <div className="bg-gray-50 border border-gray-200 p-4 rounded-xl whitespace-pre-wrap">
            {summary}
          </div>
        )}
      </div>
    </div>
  );
}
