from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
import sys
import os
import uvicorn
from pydantic import BaseModel

# Ensure we can import RAG.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import RAG
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

app = FastAPI(title="YT RAG Assistant API")

# Setup CORS, adjust origins for production if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yt-rag-frontend-830279091791.asia-south1.run.app"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage for sessions
# Format: { session_id: { 'chain': rag_chain, 'history': [] } }
sessions = {}

# Pydantic models for request bodies
class InitRequest(BaseModel):
    url: str
    api_key: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/api/init")
async def init_chat(request: InitRequest):
    video_url = request.url
    api_key = request.api_key

    if not video_url:
        raise HTTPException(status_code=400, detail="No URL provided")

    if not api_key:
        raise HTTPException(status_code=400, detail="No API key provided")

    try:
        # Set the API key for this request (used by langchain_google_genai)
        os.environ["GOOGLE_API_KEY"] = api_key

        # Initialize LLM and Embedding with the user-provided key
        llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', google_api_key=api_key)
        embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=api_key)

        # Process transcript
        print(f"Processing transcript for: {video_url}")
        transcript_chunks = RAG.process_transcript(video_url)

        if not transcript_chunks:
            raise HTTPException(status_code=400, detail="Failed to process transcript. Check if video has captions or if URL is valid.")

        # Setup RAG chain
        print("Setting up RAG chain...")
        rag_chain = RAG.setup_rag_chain(transcript_chunks, llm, embedding)

        # Create session
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            'chain': rag_chain,
            'history': []
        }

        return {
            'session_id': session_id,
            'message': 'RAG chain initialized successfully.'
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in init_chat: {e}")
        # Check for common API key errors
        error_msg = str(e)
        if "API key" in error_msg or "api_key" in error_msg or "401" in error_msg or "403" in error_msg:
            raise HTTPException(status_code=401, detail="Invalid API key. Please check your Google API key and try again.")
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/api/chat")
async def chat(request: ChatRequest):
    session_id = request.session_id
    user_message = request.message

    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=401, detail="Invalid or expired session. Please reload and enter video URL again.")

    if not user_message:
        raise HTTPException(status_code=400, detail="No message provided")

    try:
        rag_chain = sessions[session_id]['chain']

        # Invoke RAG chain
        response = rag_chain.invoke(user_message)

        # Update history
        sessions[session_id]['history'].append({'role': 'user', 'content': user_message})
        sessions[session_id]['history'].append({'role': 'ai', 'content': response})

        return {'response': response}

    except Exception as e:
        print(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

