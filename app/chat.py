
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain.chains.retrieval import create_retrieval_chain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from transformers import pipeline
from langchain_core.prompts import ChatPromptTemplate

def load_pdf_and_prepare_retriever(pdf_path,embeddings):
    # Load and split the PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    # Create a vectorstore retriever
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever()
    return retriever

def get_rag_response(user_input, pdf_path):
    
    load_dotenv()
    os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")

    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Initialize the local Hugging Face chatbot model
    chatbot_model = pipeline("text-generation", model="distilgpt2")
    retriever = load_pdf_and_prepare_retriever(pdf_path,embeddings)

    # Define the RAG system prompt and question-answer chain
    system_prompt = (
        "You are an assistant answering questions. Use the context to answer concisely."
        "\n\n{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('human', "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(chatbot_model, qa_prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # Get response
    response = rag_chain({"input": user_input})
    return response['answer']
