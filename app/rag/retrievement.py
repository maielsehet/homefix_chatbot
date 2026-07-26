import chromadb
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


#----------------------------retrieve_documents---------------------

def retrieve_documents(query, top_k=3):
    # load ChromaDB
    # chroma_client = chromadb.PersistentClient(path="Data/chroma_db")
    # collection = chroma_client.get_collection(name="homefix_db")
    
    # load embedding model
    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},   # cuda if using NVIDIA GPU
        encode_kwargs={"normalize_embeddings": True}   # normalizw vector so that better for similarity search
    )

    
    vector_store = Chroma(
        persist_directory="Data/chroma_db",
        embedding_function=embedding_model,
        collection_name="homefix_db"
    )
    print("Documents in DB:", vector_store._collection.count())


    #inside similarity query embedded happened
    results = vector_store.similarity_search(query , top_k) 
    
    return results


