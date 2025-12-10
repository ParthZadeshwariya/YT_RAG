
# 📺 YT RAG Assistant

> **Chat with any YouTube video.**
> *A powerful Retrieval-Augmented Generation (RAG) tool that turns YouTube videos into interactive knowledge bases.*

![Project Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-purple)

## 📖 Overview

**YT RAG Assistant** is an intelligent web application designed to help users extract information from YouTube videos quickly. Instead of watching hour-long tutorials or lectures, you can simply paste the video link and ask questions. The AI fetches the transcript, understands the context, and provides accurate answers based *solely* on the video content.

This project implements a full **RAG (Retrieval-Augmented Generation)** pipeline using **LangChain**, **Google Gemini**, and **FAISS**, wrapped in a modern **Flask** web application.

---

## ✨ Features

- 🎥 **Instant Video Analysis**: Fetches and processes transcripts (English & Hindi) automatically using `youtube-transcript-api`.
- 💬 **Interactive Chat Interface**: A clean, dark-themed chat UI built with glassmorphism aesthetics.
- 🧠 **Advanced RAG Engine**:
  - Uses **Google Gemini 2.5 Flash** for high-speed, intelligent responses.
  - Implements **MMR (Maximal Marginal Relevance)** search to ensure diverse and relevant context retrieval.
  - Efficient vector storage with **FAISS**.
- 🚀 **Dual Interface**:
  - **Web App**: Full-featured browser experience.
  - **CLI Tool**: Lightweight terminal version for quick queries.
- ⚡ **Real-time Processing**: Streamlined pipeline for fast ingestion and response times.

---

## 🛠️ Technology Stack

### Backend & AI
- **[Python](https://www.python.org/)**: Core programming language.
- **[Flask](https://flask.palletsprojects.com/)**: Lightweight web server.
- **[LangChain](https://www.langchain.com/)**: Framework for RAG chain orchestration.
- **[Google Generative AI](https://ai.google.dev/)**: Powered by `gemini-2.5-flash` and `embedding-001`.
- **[FAISS](https://github.com/facebookresearch/faiss)**: Fast vector similarity search.
- **[YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/)**: For extracting video captions.

### Frontend
- **HTML5 & CSS3**: Custom responsive design with modern animations and variables.
- **JavaScript (Vanilla)**: For dynamic DOM manipulation and asynchronous API calls.
- **FontAwesome**: For UI icons.
- **Google Fonts**: Uses the 'Outfit' font family.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher.
- A valid **Google API Key** (for Gemini models).

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/YT_RAG.git
   cd YT_RAG
   ```

2. **Install Dependencies**
   Run the following command to install all necessary packages:
   ```bash
   pip install flask flask-cors youtube-transcript-api langchain langchain-google-genai langchain-community faiss-cpu python-dotenv
   ```

3. **Set up Environment Variables**
   Create a `.env` file in the root directory and add your Google API key:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

---

## 🎮 Usage Guide

### Method 1: Web Application (Recommended)
Experience the full graphical interface.

1. **Run the application**:
   ```bash
   python app.py
   ```
2. **Open your browser**:
   Navigate to `http://localhost:5000`.
3. **Start Chatting**:
   - Paste a YouTube video URL in the modal.
   - Wait for the "Video Processed" confirmation.
   - Ask any question about the video!

### Method 2: Command Line Interface (CLI)
For quick, terminal-based interactions.

1. **Run the script**:
   ```bash
   python YT_RAG.py
   ```
2. **Follow the prompts**:
   - Enter the video link when asked.
   - Type your questions into the console.
   - Type `exit` to quit.

---

## 🧩 Implementation Details

How does it work under the hood?

1.  **Ingestion**: The user provides a YouTube URL. The app uses `YouTubeTranscriptApi` to download the captions.
2.  **Chunking**: The transcript is a long string of text. We use `RecursiveCharacterTextSplitter` to break it into manageable chunks (e.g., 1500 characters with overlap).
3.  **Embedding**: Each chunk is converted into a numerical vector using **Google's `embedding-001`** model. This captures the semantic meaning of the text.
4.  **Storage**: These vectors are stored in a **FAISS** index, allowing for incredibly fast similarity search.
5.  **Retrieval**: When you ask a question:
    - Your question is embedded into a vector.
    - We search the FAISS index for the most relevant transcript chunks.
    - We use **MMR** to select chunks that are relevant but not redundant.
6.  **Generation**: The relevant chunks + your question are sent to **Gemini 2.5 Flash** with a strict prompt: *"Answer only based on this context"*.
7.  **Response**: The AI generates the answer, which is sent back to the user.

---

## 📂 Project Structure

```
YT_RAG/
├── app.py                # Main Flask application entry point
├── RAG.py                # Core RAG implementation & logic library
├── YT_RAG.py             # Standalone CLI version of the tool
├── README.md             # Project documentation
├── .env                  # Environment variables (API Keys)
├── templates/
│   ├── landing.html      # Landing page template
│   └── index.html        # Main chat interface template
└── static/
    ├── css/
    │   └── styles.css    # Custom styling
    └── js/
        └── script.js     # Frontend logic
```

---

*Made with ❤️ by Parth Zadeshwariya*
