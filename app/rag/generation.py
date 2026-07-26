import os
from app.rag.retrievement import retrieve_documents
from dotenv import load_dotenv               # for get api from env 
from app.rag.prompt import build_prompt
from langchain_google_genai import ChatGoogleGenerativeAI

#--------------------------generation------------------------------
load_dotenv()
API_KEY = os.getenv("API_KEY")

# create llm once 
llm = ChatGoogleGenerativeAI(
    model="models/gemini-flash-latest",
    google_api_key=API_KEY,
    temperature=0.3
)


def generate_responce(query):
    # langchain best for this case since i use it before in retrivement so that all speak the same lang.
    retrieve_docs = retrieve_documents(query)


    # get responce 
    prompt = build_prompt(query , retrieve_docs)
    responce = llm.invoke(prompt)

    return responce.content[0]["text"]
