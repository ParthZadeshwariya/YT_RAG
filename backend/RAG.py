# --- Imports ---
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from urllib.parse import urlparse, parse_qs
from google.api_core.exceptions import ResourceExhausted, DeadlineExceeded, Aborted
from dotenv import load_dotenv


def get_youtube_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    Handles standard YouTube URLs, shortened youtu.be URLs, and embed URLs.
    """
    query = urlparse(url)

    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p.get('v', [None])[0]
        if query.path.startswith('/embed/'):
            return query.path.split('/')[2]
        if query.path.startswith('/v/'):
            return query.path.split('/')[2]
    return None



def load_dependencies():
    """Loads environment variables and initializes global models/variables."""
    load_dotenv()
    
    # Initialize the LLM and Embedding Model once
    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
    embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    return llm, embedding

from requests import Session
    
def process_transcript(video_link):
    """Fetches the transcript and splits it into LangChain documents (chunks)."""
    video_id = get_youtube_video_id(video_link)
    transcript = None

    if not video_id:
        print("Error: Invalid YouTube video link.")
        return None

    try:
        # Create a session with custom headers to prevent IP Blocks (429 Too Many Requests)
        http_client = Session()
        http_client.headers.update({
            "Accept-Language": "en-US,en;q=0.5",
        })
        ytt_api = YouTubeTranscriptApi(http_client=http_client)
        
        # Fetching the transcript data safely
        transcript_list_obj = ytt_api.list(video_id)
        
        # Try to find English or Hindi, otherwise use any available one
        try:
            transcript_obj = transcript_list_obj.find_transcript(['en', 'en-US', 'hi'])
        except:
            transcript_obj = [t for t in transcript_list_obj][0]
            
        # We DO NOT translate via YouTube API anymore to avoid 429 Too Many Requests.
        # The LLM (Gemini) handles the original language text perfectly well.
        fetched_transcript = transcript_obj.fetch()
        transcript_list = fetched_transcript.to_raw_data()
        transcript = " ".join(chunk["text"] for chunk in transcript_list)
        
    except Exception as e:
        print(f"An error occurred during transcript fetching: {e}")
        return None

    # Text Splitting (using your current parameters)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 400
    )
    chunks = splitter.create_documents([transcript])
    print(f"Transcript successfully processed into {len(chunks)} chunks.")
    return chunks

def format_docs(retrieved_docs):
    """Formats retrieved documents into a single string for the LLM context."""
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    # print(f'context: {context_text} \n\n')
    return context_text

def setup_rag_chain(transcript_chunks, llm, embedding):
    """Creates the vector store, retriever, and the runnable chain."""
    
    if not transcript_chunks:
        raise ValueError("Cannot set up RAG chain: No processed transcript chunks provided.")
        
    # Create Vector Store
    vector_store = FAISS.from_documents(transcript_chunks, embedding)
    parser = StrOutputParser()

    
    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k":6, "lambda_mult":0.9})
    
    # Define Prompt and Chain
    prompt = PromptTemplate(
        template = """
            You are an expert Q&A assistant who specializes in summarizing technical transcripts.
            Your answer **must** be entirely based** on the provided context below.
            If the context does not contain the answer, you **must** respond with "I cannot find the answer in the video but ..." then answer the question based on your knowledge.
            Elaborate your answer a bit, using a clear and professional tone.
            ---
            CONTEXT:
            {context}
            ---
            Question: {question}
            """,
        input_variables = ["context", "question"]
    )
    
    parallel_chain = RunnableParallel(
        {
            'question': RunnablePassthrough(),
            'context': retriever | RunnableLambda(format_docs)
        }
    )
    
    rag_chain = parallel_chain | prompt | llm | parser
    return rag_chain

def main_loop(rag_chain):
    """Runs the interactive loop for user queries with robust error handling."""
    if not rag_chain:
        print("Cannot start main loop: RAG chain is not initialized.")
        return

    print("\n--- RAG Assistant Initialized ---")
    print("Ask questions about the video transcript. Type 'exit' to quit.")
    print("-----------------------------------")

    while True:
        # Prompt definition is now inside the loop, though it could be outside
        # as it doesn't change, we will keep it here to mimic the original structure
        # (Note: In production, defining static objects outside the loop is better)
        
        query = input("USER: ")
        if query.lower() == 'exit':
            print('Goodbye! Have a nice day.')
            break
        
        try:
            response = rag_chain.invoke(query)
            print(f'AI: {response}\n---------------------------------------------------------------------\n')

        except ResourceExhausted:
            print("\n[AI Error]: You've reached the API's rate limit. Please wait and try again shortly.")
        except (DeadlineExceeded, Aborted):
            print("\n[AI Error]: The request timed out. The server may be busy. Please try again.")
        except Exception as e:
            # Catch all other unexpected errors (e.g., internal LangChain issues, network failures)
            print("\n[Critical AI Error]: An unexpected system error occurred.")
            print(f"Details: {type(e).__name__}: {e}")


if __name__ == "__main__":
    
    # Load Dependencies and Models
    try:
        llm, embedding = load_dependencies()
    except Exception as e:
        print(f"Initialization Error: Could not load dependencies or models. Check your .env file. Error: {e}")
        exit()

    # Process Transcript
    video_link = input("Enter video link: ")
    transcript_chunks = process_transcript(video_link)

    # Clear Exit Condition for Transcripts
    if not transcript_chunks:
        # process_transcript already printed the error reason
        exit()

    # Setup RAG Chain
    try:
        rag_chain = setup_rag_chain(transcript_chunks, llm, embedding)
    except Exception as e:
        print(f"RAG Setup Error: Failed to build the vector store or chain. Error: {e}")
        exit()

    # Run Interactive Loop
    main_loop(rag_chain)