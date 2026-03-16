import React, { useState } from 'react';

function LandingPage({ onStart, isLoading, error }) {
    const [apiKey, setApiKey] = useState('');
    const [videoUrl, setVideoUrl] = useState('');
    const [showKey, setShowKey] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        onStart(apiKey.trim(), videoUrl.trim());
    };

    const features = [
        {
            icon: 'fa-solid fa-brain',
            title: 'AI-Powered Q&A',
            desc: 'Ask any question and get accurate answers grounded in the video transcript.',
        },
        {
            icon: 'fa-solid fa-video',
            title: 'Watch & Chat',
            desc: 'Watch the video and chat with the AI side-by-side in a seamless interface.',
        },
        {
            icon: 'fa-solid fa-bolt',
            title: 'Instant Analysis',
            desc: 'Powered by advanced RAG pipeline for fast, context-aware responses.',
        },
    ];

    return (
        <div className="landing-page">
            {/* Animated background */}
            <div className="landing-bg">
                <div className="bg-orb orb-landing-1"></div>
                <div className="bg-orb orb-landing-2"></div>
                <div className="bg-orb orb-landing-3"></div>
                <div className="bg-grid"></div>
            </div>

            <div className="landing-content">
                {/* Hero Section */}
                <section className="hero-section">
                    <div className="hero-badge">
                        <i className="fa-solid fa-sparkles"></i>
                        <span>AI-Powered Video Intelligence</span>
                    </div>

                    <h1 className="hero-title">
                        Chat with any
                        <span className="gradient-text"> YouTube </span>
                        video
                    </h1>

                    <p className="hero-subtitle">
                        Paste a YouTube link, provide your API key, and start asking questions.
                        Our AI analyzes the transcript and gives you instant, accurate answers.
                    </p>
                </section>

                {/* Form Card */}
                <section className="setup-card">
                    <form onSubmit={handleSubmit} autoComplete="off">
                        {/* API Key Input */}
                        <div className="form-group">
                            <label htmlFor="api-key-input">
                                <i className="fa-solid fa-key"></i>
                                Google API Key
                            </label>
                            <div className="input-group">
                                <input
                                    id="api-key-input"
                                    type={showKey ? 'text' : 'password'}
                                    placeholder="Enter your Google Gemini API key"
                                    value={apiKey}
                                    onChange={(e) => setApiKey(e.target.value)}
                                    disabled={isLoading}
                                    required
                                />
                                <button
                                    type="button"
                                    className="toggle-visibility-btn"
                                    onClick={() => setShowKey(!showKey)}
                                    tabIndex={-1}
                                    title={showKey ? 'Hide key' : 'Show key'}
                                >
                                    <i className={`fa-solid ${showKey ? 'fa-eye-slash' : 'fa-eye'}`}></i>
                                </button>
                            </div>
                            <span className="form-hint">
                                <i className="fa-solid fa-shield-halved"></i>
                                Your key is used for this session only and never stored.
                            </span>
                        </div>

                        {/* YouTube URL Input */}
                        <div className="form-group">
                            <label htmlFor="video-url-input">
                                <i className="fa-brands fa-youtube"></i>
                                YouTube Video URL
                            </label>
                            <div className="input-group">
                                <input
                                    id="video-url-input"
                                    type="url"
                                    placeholder="https://www.youtube.com/watch?v=..."
                                    value={videoUrl}
                                    onChange={(e) => setVideoUrl(e.target.value)}
                                    disabled={isLoading}
                                    required
                                />
                            </div>
                        </div>

                        {/* Error Message */}
                        {error && (
                            <div className="error-banner" id="init-error">
                                <i className="fa-solid fa-circle-exclamation"></i>
                                <span>{error}</span>
                            </div>
                        )}

                        {/* Submit Button */}
                        <button
                            type="submit"
                            className="submit-btn"
                            id="analyze-btn"
                            disabled={isLoading || !apiKey.trim() || !videoUrl.trim()}
                        >
                            {isLoading ? (
                                <>
                                    <div className="spinner"></div>
                                    <span>Analyzing Video...</span>
                                </>
                            ) : (
                                <>
                                    <i className="fa-solid fa-play"></i>
                                    <span>Analyze Video</span>
                                </>
                            )}
                        </button>
                    </form>
                </section>

                {/* Feature Cards */}
                <section className="features-section">
                    {features.map((f, i) => (
                        <div className="feature-card" key={i} style={{ animationDelay: `${i * 0.1}s` }}>
                            <div className="feature-icon">
                                <i className={f.icon}></i>
                            </div>
                            <h3>{f.title}</h3>
                            <p>{f.desc}</p>
                        </div>
                    ))}
                </section>

                {/* Footer */}
                <footer className="landing-footer">
                    <p>
                        Built with <i className="fa-solid fa-heart" style={{ color: '#ef4444' }}></i> using LangChain, FAISS & Google Gemini
                    </p>
                </footer>
            </div>
        </div>
    );
}

export default LandingPage;
