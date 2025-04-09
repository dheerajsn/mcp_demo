import os
import glob
import argparse
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def create_vector_db(documents, save_local=False):
    """Create a vector database from documents."""
    try:
        if not documents:
            return
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level from src to the project root
        project_root = os.path.abspath(os.path.join(current_dir, ".."))

        # Navigate to the db directory from the project root
        db_dir = os.path.join(project_root, "faiss_db")
        # Create directory if it doesn't exist
        os.makedirs(db_dir, exist_ok=True)
        
        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        text_chunks = text_splitter.split_documents(documents)
        
        # Create embeddings with MiniLM-L6-v2 model
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        model_kwargs = {'device': 'cpu'}
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs
        )
        
        # Create FAISS vector store")
        vector_db = FAISS.from_documents(
            documents=text_chunks,
            embedding=embeddings
        )
        
        # Save FAISS index to disk
        faiss_path = os.path.join(db_dir, "faiss_index")
        if save_local:
            vector_db.save_local(faiss_path)
        
        return vector_db
    except Exception as e:
        return None