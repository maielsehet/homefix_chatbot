from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
#--------------------vector database and embeddinds --------------------
def create_and_store_embeddings(documents):

    # load model   --> this suitable for arabic , eng , frach 
    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},   # cuda if using NVIDIA GPU
        encode_kwargs={"normalize_embeddings": True}   # normalizw vector so that better for similarity search
    )



    # collection ---> use once whrn creating db
    #  chroma only for open an existing one 
    collection = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory="Data/chroma_db",
        collection_name="homefix_db"
    )

    
    print("Embeddings stored successfully")
    return collection


