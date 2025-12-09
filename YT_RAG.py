from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from urllib.parse import urlparse, parse_qs
from google.api_core.exceptions import ResourceExhausted, DeadlineExceeded, Aborted
from dotenv import load_dotenv

load_dotenv()

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

video_link = input("enter video link: ")
video_id = get_youtube_video_id(video_link)

try:
    fetched_transcript = YouTubeTranscriptApi().fetch(video_id, languages=['en', 'hi'])
    transcript_list = fetched_transcript.to_raw_data()
    transcript = " ".join(chunk["text"] for chunk in transcript_list)
    # print(transcript)
   
except TranscriptsDisabled:
    print("No captions available for this video.")
except Exception as e:
    print(f"An error occurred: {e}")





splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 400
)
chunks = splitter.create_documents([transcript])

embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

vector_store = FAISS.from_documents(chunks, embedding)

parser = StrOutputParser()

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

# Contextual Compression: Use a component like LangChain's Contextual Compression (e.g., LLMChainExtractor) to prune the retrieved chunks, removing sentences that are irrelevant to the specific user question before sending them to the final LLM prompt. This drastically reduces noise and improves LLM focus.
# compressor = LLMChainExtractor.from_llm(llm=llm)

# base_retriever = vector_store.as_retriever(
#     search_type="mmr", 
#     search_kwargs={"k": 6, "lambda_mult": 0.7} 
# )

# retriever = ContextualCompressionRetriever(
#     base_compressor=compressor, 
#     base_retriever=base_retriever
# )

retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k":6, "lambda_mult":0.9})

def format_docs(retrieved_docs):
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    # print(f'context: {context_text} \n\n')
    return context_text


##################################################



while True:
    prompt = PromptTemplate(
        template = """
            You are an expert Q&A assistant who specializes in summarizing technical transcripts.
            Your answer **must** be entirely based** on the provided context below.
            If the context does not contain the answer, you **must** respond with "I cannot find the answer in the video."
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

    # add try except to handle errors
    chain = parallel_chain | prompt | llm | parser

    query = input("USER: ")
    if query.lower() == 'exit':
        print('Goodbye! Have a nice day.')
        break
    
    try:
        # The invocation point where most errors will occur
        print(f'AI: {chain.invoke(query)}\n---------------------------------------------------------------------\n')

    except ResourceExhausted:
        print("\n[AI Error]: You've reached the API's rate limit. Please wait and try again shortly.")
    except (DeadlineExceeded, Aborted):
        print("\n[AI Error]: The request timed out. The server may be busy. Please try again.")
    except Exception as e:
        # Catch all other unexpected errors (e.g., internal LangChain issues, network failures)
        print("\n[Critical AI Error]: An unexpected system error occurred.")
        print(f"Details: {type(e).__name__}: {e}")

    