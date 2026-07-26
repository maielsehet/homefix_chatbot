from rag.embeddind import create_and_store_embeddings
from utils.functions import generate_documents,save_documents
import sys
sys.stdout.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    documents = generate_documents()
    save_documents(documents)
    vector_store = create_and_store_embeddings(documents)
    print("Stored:", vector_store._collection.count())