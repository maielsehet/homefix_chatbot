-----------------------------
# from langchain_core import documents
# import pandas as pd 
# import re   
# import os

# #----------------------------cleaning stage --------------------------
# #  remove spaces and unwanted punctuation
# def clean(data):
#     text = re.sub(r'[().،:]', '' , data)
#     # remove unneeded spaces
#     text = re.sub(r'\s+' , ' ' ,text)
#     return text.strip()


# #  prepare the result
# def processed(row):
#     problem = f"المشكله: {clean(row['problem'])} "
#     category = f"النوع: {clean(row['category'])} "
#     solution = f"الحل: {clean(row['solution'])} "
#     # print(problem)
#     # print(category)
#     # print(solution)
#     return problem + category + solution



# def cleaning_data():
#     #  to get file 
#     path_from = 'Data/CSV files/'
#     path_to = 'Data/Processed/'


#     #  get files 
#     files = [f for f in os.listdir(path_from) if f.endswith('.csv')]
#     # files = ['اجهزة صغيرة' ,'السخان' ,'تكييف' , 'تلاجات' , 'حدادة' , 
#     #         'خلاط وميكروووف و بوتجااز' , 'سباكه' , 'شاشات' , 'غسالات' ,
#     #         'كهرباء و مراوح' , 'نجاره' ,'نقاشه']


#     for file in files:
#         source = os.path.join(path_from, file)
#         destination = os.path.join(path_to, os.path.splitext(file)[0] + '.txt')

#         # create a dataframe
#         df = pd.read_csv(source , encoding='utf-8-sig')

#         #  drop dublicates
#         df.drop_duplicates(inplace=True)

#         # apply clean on data 
#         df['problem'] = df['problem'].apply(clean)
#         df['category'] = df['category'].apply(clean)
#         df['solution'] = df['solution'].apply(clean)



#         # axis=1 ---> for apply on rows
#         cleaned_data = df.apply(processed , axis=1)

#         # add the cleand part to proceeded folder
#         try:
#             with open(destination , 'w' , encoding='utf-8-sig') as f:
#                 #  use join since wite need string not series 
#                 f.write(''.join(cleaned_data))  
#         except (FileExistsError):
#             print(f"file {destination} exists.")



# #------------------------------------------------------------------------
# #Document & Metadata
# from langchain_core.documents import Document
# import glob
# file="Data/Processed"
# file_paths=glob.glob(os.path.join(file, "*.txt"))
# documents = []
# for path in file_paths:
#     with open(path, 'r', encoding='utf-8-sig') as f:
#         content = f.read()
#     doc=Document(
#         page_content=content,
#         metadata={"source":os.path.basename(path)}
#         )
#     documents.append(doc)
#     # append  documents into Data\Documents
#     with open("Data/Documents/documents.txt", "a", encoding='utf-8-sig') as f:
#         f.write(f"source: {os.path.basename(path)}\n")
#         f.write(content)
#         f.write("\n\n")

# print("number of documents:" ,len(documents))   
# #------------------------------------------------------------------------


import os
import re
import glob
import pandas as pd
from langchain_core.documents import Document

# -----------------------------------------------------
# Cleaning Functions
# -----------------------------------------------------

def clean(text):
    """Clean Arabic text."""
    if pd.isna(text):
        return ""

    text = str(text)

    # Remove unwanted punctuation
    text = re.sub(r"[().،:]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -----------------------------------------------------
# Convert one row into one Document
# -----------------------------------------------------

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


# -----------------------------------------------------
# Main Pipeline
<<<<<<< HEAD
# -----------------------------------------------------
=======
# ------------------------
>>>>>>> 88482a3a227151341213db34e571729965914eb6

def generate_documents():

    csv_folder = "Data/CSV files"

    documents = []

    csv_files = glob.glob(os.path.join(csv_folder, "*.csv"))

    for csv_file in csv_files:

        df = pd.read_csv(csv_file, encoding="utf-8-sig")

        # Remove duplicates
        df = df.drop_duplicates()

        # Clean columns
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


# -----------------------------------------------------
# Save documents for debugging (Optional)
# -----------------------------------------------------

def save_documents(documents):

    os.makedirs("Data/Documents", exist_ok=True)

    output_path = "Data/Documents/documents.txt"

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


<<<<<<< HEAD
# -----------------------------------------------------
# Run
# -----------------------------------------------------

if __name__ == "__main__":

    documents = generate_documents()

    save_documents(documents)
=======



>>>>>>> 88482a3a227151341213db34e571729965914eb6

# ----------------------------------------------------
# vector database & embeddinds 
#-----------------------------------------------------
<<<<<<< HEAD
from fastembed import TextEmbedding
import chromadb

def create_and_store_embeddings(documents, collection_name="homefix_knowledge_base"):
    # Load fast embedding model
    embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    # Setup chroma db client
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection(name=collection_name)
    
    # Prepare texts, metadatas, and ids
    texts = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]
    ids = [f"doc_{i+1}" for i in range(len(documents))]
    
    # Generate embeddings
    embeddings = list(embedding_model.embed(texts))
    embeddings = [e.tolist() for e in embeddings]
    
    # Store in chroma
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    print("Embeddings stored successfully")
    return collection
=======
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def create_and_store_embeddings(documents):

    # Load multilingual embedding model
    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},   # Change to "cuda" if using NVIDIA GPU
        encode_kwargs={"normalize_embeddings": True}
    )

    # Create Chroma Vector Store
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory="Data/chroma_db",
        collection_name="homefix_knowledge_base"
    )

    print("Embeddings stored successfully!")

    return vector_store


if name == "main":

    documents = generate_documents()

    save_documents(documents)  
    vector_store = create_and_store_embeddings(documents)
>>>>>>> 88482a3a227151341213db34e571729965914eb6
