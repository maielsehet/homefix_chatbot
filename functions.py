

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
from app.rag.embeddind import create_and_store_embeddings
from langchain_core.documents import Document
from app.rag.generation import generate_responce
import sys
sys.stdout.reconfigure(encoding="utf-8")

# -----------------------cleaning------------------------------

def clean(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # remove unwanted punctuation
    text = re.sub(r"[().،:]", "", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# --------------------------Convert one row into one Document---------------------------

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
        "source": source_file,
        "row_id": row_id
    }

    return Document(
        page_content=page_content.strip(),
        metadata=metadata
    )


# ----------------------------generate documents-------------------------

def generate_documents():

    csv_folder = "Data/CSV files"

    documents = []

    # get all csv files 
    csv_files = glob.glob(os.path.join(csv_folder, "*.csv"))

    for csv_file in csv_files:

        df = pd.read_csv(csv_file, encoding="utf-8-sig")

        # remove duplicates
        df = df.drop_duplicates()
        # 0,1,2,3, after drop null will be for ex: 0,1,3,4,7 this return index agsin
        df.reset_index(drop=True)

        # clean columns
        df["problem"] = df["problem"].apply(clean)
        df["category"] = df["category"].apply(clean)
        df["solution"] = df["solution"].apply(clean)

        #  get sourse naem
        source_name = os.path.basename(csv_file)

        for index, row in df.iterrows():

            document = row_to_document(
                row=row,
                source_file=source_name,
                row_id=int(index)   #numpy.int64 
            )

            documents.append(document)

    print(f"total documents: {len(documents)}")

    return documents


# ------------------save documents-------------------
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







# ----------------------------------------------------
# vector database & embeddinds 
#-----------------------------------------------------
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
        collection_name="homefix_db"
    )

    print("Embeddings stored successfully!")

    return vector_store


if __name__ == "__main__":

    # if not os.path.exists("Data/chroma_db"):
    documents = generate_documents()
    save_documents(documents)
    vector_store = create_and_store_embeddings(documents)
    print("Stored:", vector_store._collection.count())



    query = "السخان لا يسخن"
    response = generate_response(query)
    print(response)

