document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const elements = {
        modal: document.getElementById('url-modal'),
        urlInput: document.getElementById('url-input'),
        initBtn: document.getElementById('init-btn'),
        initSpinner: document.getElementById('init-spinner'),
        errorMsg: document.getElementById('error-msg'),
        chatContainer: document.getElementById('chat-container'),
        userInput: document.getElementById('user-input'),
        sendBtn: document.getElementById('send-btn'),
        resetBtn: document.getElementById('reset-btn'),
        welcomeMsg: document.querySelector('.welcome-message')
    };

    // State
    let sessionId = null;

    // --- Functions ---

    // Show/Hide specific UI states
    const toggleLoading = (isLoading) => {
        elements.initBtn.disabled = isLoading;
        if (isLoading) {
            elements.initSpinner.classList.remove('hidden');
        } else {
            elements.initSpinner.classList.add('hidden');
        }
    };

    const toggleChatInput = (isEnabled) => {
        elements.userInput.disabled = !isEnabled;
        elements.sendBtn.disabled = !isEnabled;
        if (isEnabled) elements.userInput.focus();
    };

    const showError = (msg) => {
        elements.errorMsg.textContent = msg;
        elements.errorMsg.classList.remove('hidden');
    };

    const addMessage = (role, content, isThinking = false) => {
        // Remove welcome message if it exists
        if (elements.welcomeMsg) {
            elements.welcomeMsg.remove();
            delete elements.welcomeMsg; // Prevent re-querying
        }

        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;

        if (isThinking) {
            msgDiv.innerHTML = `
                <div class="thinking-dots">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
                <span>Thinking...</span>
            `;
            msgDiv.id = 'thinking-msg';
        } else {
            // Check if marked is available, otherwise fallback to plain text
            if (typeof marked !== 'undefined') {
                msgDiv.innerHTML = marked.parse(content);
            } else {
                msgDiv.textContent = content;
            }
        }

        elements.chatContainer.appendChild(msgDiv);
        elements.chatContainer.scrollTop = elements.chatContainer.scrollHeight;
    };

    const removeThinkingMessage = () => {
        const thinkingMsg = document.getElementById('thinking-msg');
        if (thinkingMsg) {
            thinkingMsg.remove();
        }
    };

    // --- API Interactions ---

    const initSession = async () => {
        const url = elements.urlInput.value.trim();
        if (!url) {
            showError("Please enter a YouTube URL");
            return;
        }

        toggleLoading(true);
        elements.errorMsg.classList.add('hidden');

        try {
            const response = await fetch('/api/init', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to initialize');
            }

            sessionId = data.session_id;
            elements.modal.classList.add('hidden');
            toggleChatInput(true);
            addMessage('ai', 'I have analyzed the video. Ask me anything about it!');

        } catch (error) {
            showError(error.message);
        } finally {
            toggleLoading(false);
        }
    };

    const sendMessage = async () => {
        const message = elements.userInput.value.trim();
        if (!message || !sessionId) return;

        // Add User Message
        addMessage('user', message);
        elements.userInput.value = '';

        // Add Thinking Placeholder
        addMessage('ai', null, true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: sessionId,
                    message: message
                })
            });

            const data = await response.json();

            // Remove Thinking Placeholder
            removeThinkingMessage();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to get response');
            }

            addMessage('ai', data.response);

        } catch (error) {
            removeThinkingMessage();
            addMessage('ai', `Error: ${error.message}`);
        }
    };

    // --- Event Listeners ---

    if (elements.initBtn) {
        elements.initBtn.addEventListener('click', initSession);
        elements.urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') initSession();
        });
        // Handle Input Focus for easier typing
        elements.urlInput.focus();
    }

    elements.sendBtn.addEventListener('click', sendMessage);

    elements.userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    elements.resetBtn.addEventListener('click', () => {
        location.reload(); // Simple way to reset state
    });

});
