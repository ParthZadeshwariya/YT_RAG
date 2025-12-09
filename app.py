from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import uuid
import sys
import os

# Ensure we can import RAG.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import RAG

app = Flask(__name__)
CORS(app)

# Global storage for sessions
# Format: { session_id: { 'chain': rag_chain, 'history': [] } }
sessions = {}

# Load dependencies once at startup
try:
    print("Loading global models...")
    llm, embedding = RAG.load_dependencies()
    print("Global models loaded successfully.")
except Exception as e:
    print(f"Critical Error: Failed to load dependencies: {e}")
    sys.exit(1)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/app')
def app_route():
    return render_template('index.html')

@app.route('/api/init', methods=['POST'])
def init_chat():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        # Process transcript
        print(f"Processing transcript for: {video_url}")
        transcript_chunks = RAG.process_transcript(video_url)
        
        if not transcript_chunks:
            return jsonify({'error': 'Failed to process transcript. Check if video has captions or if URL is valid.'}), 400
            
        # Setup RAG chain
        print("Setting up RAG chain...")
        rag_chain = RAG.setup_rag_chain(transcript_chunks, llm, embedding)
        
        # Create session
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            'chain': rag_chain,
            'history': []
        }
        
        return jsonify({
            'session_id': session_id,
            'message': 'RAG chain initialized successfully.'
        })
        
    except Exception as e:
        print(f"Error in init_chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id')
    user_message = data.get('message')
    
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid or expired session. Please reload and enter video URL again.'}), 401
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
        
    try:
        rag_chain = sessions[session_id]['chain']
        
        # Invoke RAG chain
        response = rag_chain.invoke(user_message)
        
        # Update history (optional, for future use)
        sessions[session_id]['history'].append({'role': 'user', 'content': user_message})
        sessions[session_id]['history'].append({'role': 'ai', 'content': response})
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
