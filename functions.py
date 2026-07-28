import os
import re
import glob
import pandas as pd
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ---------------------------------------clean text------------------------
def clean(text):
   
    if pd.isna(text):
        return ""

    text = str(text)

    # remove unwanted punctuation
    text = re.sub(r"[().،:]", "", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ------------------------ convert row into Document -----------------------------

def row_to_document(row, source_file, row_id):
    page_content = f"""
النوع:
{row["category"]}

المشكلة:
{row["problem"]}

الحل:
{row["solution"]}
"""

    metadata = {
        "category": row["category"],
        "device": row["category"],
        "source": source_file,
        "row_id": row_id
    }

    return Document(
        page_content=page_content.strip(),
        metadata=metadata
    )



# ----------------------generate_documents------------------------------- 

def generate_documents():
    #  get allcsv files
    csv_folder = "Data/CSV files"

    documents = []
    #  get allcsv files
    csv_files = glob.glob(os.path.join(csv_folder, "*.csv"))

    for csv_file in csv_files:

        df = pd.read_csv(csv_file, encoding="utf-8-sig")

        # remove duplicates
        df = df.drop_duplicates()

        # rlean columns
        df["problem"] = df["problem"].apply(clean)
        df["category"] = df["category"].apply(clean)
        df["solution"] = df["solution"].apply(clean)

        source_name = os.path.basename(csv_file)

        for index, row in df.iterrows():

            document = row_to_document(
                row=row,
                source_file=source_name,
                row_id=index
            )

            documents.append(document)

    print(f"Total Documents: {len(documents)}")

    return documents


# ----------------------save_documents-------------------------------

def save_documents(documents):
    #  create dir
    os.makedirs("Data/Documents", exist_ok=True)

    output_path = "Data/Documents/documents.txt"

    # utf-8-sig ---> arabic 
    with open(output_path, "w", encoding="utf-8-sig") as f:

        for i, doc in enumerate(documents):

            f.write("=" * 70 + "\n")
            f.write(f"Document #{i+1}\n\n")

            f.write("Metadata\n")
            f.write(str(doc.metadata))
            f.write("\n\n")

            f.write("Content\n")
            f.write(doc.page_content)
            f.write("\n\n")



# -----------------------------------------------------

if __name__ == "__main__":

    documents = generate_documents()

    save_documents(documents)





#----------------------------vector database & embeddinds -------------------------

from fastembed import TextEmbedding
import chromadb

def create_and_store_embeddings(documents, collection_name="homefix_knowledge_base"):
    # load fast embedding model
    embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    # setup chroma db client
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection(name=collection_name)
    
    # prepare text metadatasand ids
    texts = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]
    ids = [f"doc_{i+1}" for i in range(len(documents))]
    
    # generate embeddings
    embeddings = list(embedding_model.embed(texts))
    embeddings = [e.tolist() for e in embeddings]
    
    # store in chroma
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    print("Embeddings stored successfully")
    return collection



# ------------------------------------create_and_store_embeddings------------------------------------

def create_and_store_embeddings(documents):

    # load multilingual embedding model
    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},   # "cuda" if using NVIDIA GPU
        encode_kwargs={"normalize_embeddings": True}
    )


    # create vector db
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory="Data/chroma_db",
        collection_name="homefix_knowledge_base"
    )


    print("Embeddings stored successfully!")

    return vector_store


if __name__ == "main":

    documents = generate_documents()

    save_documents(documents)  
    vector_store = create_and_store_embeddings(documents)
