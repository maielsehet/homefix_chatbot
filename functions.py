import os
import re
import glob
import pandas as pd
from app.rag.embeddind import create_and_store_embeddings
from langchain_core.documents import Document
from app.rag.generation import generate_responce

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




if __name__ == "__main__":

    if not os.path.exists("Data/chroma_db"):
        documents = generate_documents()
        save_documents(documents)
        vector_store = create_and_store_embeddings(documents)


    query = "السخان لا يسخن"
    response = generate_responce(query)
    print(response)