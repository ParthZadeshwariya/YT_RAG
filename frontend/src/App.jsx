import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import ChatInterface from './components/ChatInterface';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

function App() {
  const [view, setView] = useState('landing'); // 'landing' | 'chat'
  const [sessionId, setSessionId] = useState(null);
  const [videoUrl, setVideoUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleStart = async (apiKey, url) => {
    if (!apiKey || !url) {
      setError('Please fill in both fields.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE_URL}/api/init`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, api_key: apiKey }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || data.error || 'Failed to initialize session');
      }

      setSessionId(data.session_id);
      setVideoUrl(url);
      setView('chat');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setView('landing');
    setSessionId(null);
    setVideoUrl('');
    setError('');
  };

  return (
    <>
      {view === 'landing' && (
        <LandingPage
          onStart={handleStart}
          isLoading={isLoading}
          error={error}
        />
      )}
      {view === 'chat' && (
        <ChatInterface
          sessionId={sessionId}
          videoUrl={videoUrl}
          onReset={handleReset}
        />
      )}
    </>
  );
}

export default App;
