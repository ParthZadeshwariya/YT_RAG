
# 📺 YT RAG Assistant

> **Chat with any YouTube video.**
> *A powerful Retrieval-Augmented Generation (RAG) tool that turns YouTube videos into interactive knowledge bases.*

**[🚀 Try the Live App](https://yt-rag-frontend-830279091791.asia-south1.run.app)**


![Project Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-19.0-61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![License](https://img.shields.io/badge/License-MIT-purple)

## 📖 Overview

**YT RAG Assistant** is an intelligent web application designed to help users extract information from YouTube videos quickly. Instead of watching hour-long tutorials or lectures, you can simply paste the video link and ask questions. The AI fetches the transcript, understands the context, and provides accurate answers based *solely* on the video content.

This project implements a full **RAG (Retrieval-Augmented Generation)** pipeline using **LangChain**, **Google Gemini**, and **FAISS**, with a split architecture: a **FastAPI** backend and a **React/Vite** frontend.

---

## ✨ Features

- 🎥 **Instant Video Analysis**: Fetches and processes transcripts (English & Hindi) automatically using `youtube-transcript-api`.
- 💬 **Interactive Chat Interface**: A modern, responsive React-based chat UI with markdown support and smooth animations.
- 🧠 **Advanced RAG Engine**:
  - Uses **Google Gemini 2.5 Flash** for high-speed, intelligent responses.
  - Implements **MMR (Maximal Marginal Relevance)** search to ensure diverse and relevant context retrieval.
  - Efficient vector storage with **FAISS**.
- 🚀 **Dual Interface**:
  - **Modern Web App**: Built with React and Vite for a premium user experience. **[Live Demo](https://yt-rag-frontend-830279091791.asia-south1.run.app)**
  - **CLI Tool**: Lightweight terminal version for quick queries.
- ⚡ **Real-time Processing**: Streamlined pipeline for fast ingestion and response times.

---

## 🛠️ Technology Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)**: High-performance Python web framework.
- **[LangChain](https://www.langchain.com/)**: Framework for RAG chain orchestration.
- **[Google Generative AI](https://ai.google.dev/)**: Powered by `gemini-2.5-flash` and `embedding-001`.
- **[FAISS](https://github.com/facebookresearch/faiss)**: Fast vector similarity search.
- **[YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/)**: For extracting video captions.

### Frontend
- **[React](https://react.dev/)**: For building the interactive user interface.
- **[Vite](https://vitejs.dev/)**: Next-generation frontend tooling.
- **[React Markdown](https://github.com/remarkjs/react-markdown)**: For rendering AI responses with formatting.
- **Vanilla CSS**: Custom professional styling with modern variables and animations.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js & npm
- A valid **Google API Key** (for Gemini models).

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ParthZadeshwariya/YT_RAG.git
   cd YT_RAG
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install fastapi uvicorn youtube-transcript-api langchain langchain-google-genai langchain-community faiss-cpu python-dotenv pydantic
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

---

## 🎮 Usage Guide

### 1. Start the Backend API
Run the FastAPI server (default port 8000):
```bash
cd backend
python app.py
```

### 2. Start the Frontend
Run the Vite development server:
```bash
cd frontend
npm run dev
```
Open your browser and navigate to the local URL (usually `http://localhost:5173`).

### 3. CLI Mode
For quick, terminal-based interactions:
```bash
cd backend
python YT_RAG.py
```

---

## 🧩 Implementation Details

1.  **Ingestion**: The user provides a YouTube URL. The app uses `YouTubeTranscriptApi` to download the captions.
2.  **Chunking**: The transcript is processed into manageable segments using `RecursiveCharacterTextSplitter`.
3.  **Embedding**: Each chunk is converted into a numerical vector using **Google's `embedding-001`** model.
4.  **Storage**: Vectors are stored in **FAISS**, allowing for millisecond-speed similarity search.
5.  **Retrieval & Generation**: When a question is asked, the most relevant chunks are retrieved via **MMR** and passed to **Gemini 2.5 Flash** to generate a contextual response.

---

## 📂 Project Structure

```text
YT_RAG/
├── backend/               # Python FastAPI backend
│   ├── app.py             # FastAPI entry point
│   ├── RAG.py             # Core RAG logic library
│   └── YT_RAG.py          # Standalone CLI version
├── frontend/              # React Vite frontend
│   ├── src/               # React source files
│   ├── public/            # Static assets
│   └── package.json       # Frontend dependencies
├── README.md              # Project documentation
└── .gitignore             # Global git exclusions
```

---

*Made with ❤️ by Parth Zadeshwariya*

