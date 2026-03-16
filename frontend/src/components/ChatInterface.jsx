import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

const API_BASE_URL = 'http://127.0.0.1:8000';

function ChatInterface({ sessionId, videoUrl, onReset }) {
    const [messages, setMessages] = useState([
        { role: 'ai', content: '👋 I\'ve analyzed the video! Ask me anything about its content.' },
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isThinking, setIsThinking] = useState(false);
    const chatEndRef = useRef(null);
    const inputRef = useRef(null);

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isThinking]);

    useEffect(() => {
        inputRef.current?.focus();
    }, []);

    // Extract video ID from URL for embed
    const getVideoId = (url) => {
        try {
            const parsed = new URL(url);
            if (parsed.hostname === 'youtu.be') return parsed.pathname.slice(1);
            if (parsed.hostname.includes('youtube.com')) {
                if (parsed.pathname === '/watch') return parsed.searchParams.get('v');
                if (parsed.pathname.startsWith('/embed/')) return parsed.pathname.split('/')[2];
            }
        } catch { }
        return null;
    };

    const videoId = getVideoId(videoUrl);

    const handleSendMessage = async () => {
        if (!inputValue.trim() || !sessionId) return;

        const userMsg = inputValue.trim();
        setInputValue('');
        setMessages((prev) => [...prev, { role: 'user', content: userMsg }]);
        setIsThinking(true);

        try {
            const response = await fetch(`${API_BASE_URL}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId, message: userMsg }),
            });

            const data = await response.json();
            setIsThinking(false);

            if (!response.ok) {
                throw new Error(data.detail || data.error || 'Failed to get response');
            }

            setMessages((prev) => [...prev, { role: 'ai', content: data.response }]);
        } catch (error) {
            setIsThinking(false);
            setMessages((prev) => [
                ...prev,
                { role: 'ai', content: `⚠️ Error: ${error.message}` },
            ]);
        }
    };

    return (
        <div className="chat-page">
            {/* Background */}
            <div className="chat-bg">
                <div className="bg-orb orb-chat-1"></div>
                <div className="bg-orb orb-chat-2"></div>
            </div>

            {/* Top Bar */}
            <header className="chat-header">
                <div className="chat-header-left">
                    <div className="logo-mini">
                        <i className="fa-brands fa-youtube"></i>
                        <span>YT RAG</span>
                    </div>
                </div>
                <button className="new-session-btn" id="new-session-btn" onClick={onReset} title="New Session">
                    <i className="fa-solid fa-plus"></i>
                    <span>New Session</span>
                </button>
            </header>

            {/* Main Content: Video + Chat side by side */}
            <div className="chat-layout">
                {/* Left: Video Player */}
                <div className="video-panel">
                    <div className="video-container">
                        {videoId ? (
                            <iframe
                                id="video-player"
                                src={`https://www.youtube.com/embed/${videoId}?rel=0`}
                                title="YouTube Video Player"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                                allowFullScreen
                            ></iframe>
                        ) : (
                            <div className="video-placeholder">
                                <i className="fa-solid fa-film"></i>
                                <p>Could not load video preview</p>
                            </div>
                        )}
                    </div>

                    {/* Video info under the player */}
                    <div className="video-info-bar">
                        <i className="fa-solid fa-circle-check"></i>
                        <span>Transcript analyzed & ready</span>
                    </div>
                </div>

                {/* Right: Chat */}
                <div className="chat-panel">
                    {/* Messages */}
                    <div className="chat-messages" id="chat-messages">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`chat-bubble ${msg.role}`}>
                                <div className="bubble-avatar">
                                    {msg.role === 'ai' ? (
                                        <i className="fa-solid fa-robot"></i>
                                    ) : (
                                        <i className="fa-solid fa-user"></i>
                                    )}
                                </div>
                                <div className="bubble-content">
                                    {msg.role === 'ai' ? (
                                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                                    ) : (
                                        <p>{msg.content}</p>
                                    )}
                                </div>
                            </div>
                        ))}

                        {isThinking && (
                            <div className="chat-bubble ai" id="thinking-bubble">
                                <div className="bubble-avatar">
                                    <i className="fa-solid fa-robot"></i>
                                </div>
                                <div className="bubble-content">
                                    <div className="thinking-indicator">
                                        <div className="thinking-dot"></div>
                                        <div className="thinking-dot"></div>
                                        <div className="thinking-dot"></div>
                                    </div>
                                </div>
                            </div>
                        )}

                        <div ref={chatEndRef} />
                    </div>

                    {/* Chat Input */}
                    <div className="chat-input-area">
                        <div className="chat-input-wrapper">
                            <input
                                ref={inputRef}
                                type="text"
                                id="chat-input"
                                placeholder="Ask about the video..."
                                autoComplete="off"
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                                disabled={isThinking}
                            />
                            <button
                                id="send-msg-btn"
                                className="send-btn"
                                disabled={!inputValue.trim() || isThinking}
                                onClick={handleSendMessage}
                            >
                                <i className="fa-solid fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ChatInterface;
