# from app.rag.retrievement import retrieve_documents
# from app.rag.prompt import build_prompt
# from app.rag.clarification import clarify_query
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# import os

# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="models/gemini-flash-latest",
#     google_api_key=os.getenv("API_KEY"),
#     temperature=0.3
# )

# def extract_text(response):

#     content = response.content

#     if isinstance(content, str):
#         return content.strip()

#     if isinstance(content, list):

#         text = ""

#         for part in content:

#             if isinstance(part, dict):
#                 text += part.get("text", "")

#             elif hasattr(part, "text"):
#                 text += part.text

#             else:
#                 text += str(part)

#         return text.strip()

#     return str(content).strip()

# def generate_response(conversation_history):

   
#     last_query = conversation_history[-1]["content"]

    
#     history_text = ""

#     for message in conversation_history:
#         history_text += f"{message['role']}: {message['content']}\n"

#     clarification = clarify_query(history_text)

#     if clarification != "READY":
#         return clarification

#     docs = retrieve_documents(history_text)

#     prompt = build_prompt(history_text, docs)

#     response = llm.invoke(prompt)
    

#     return extract_text(response)



import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from app.rag.clarification import clarify_query
from app.rag.prompt import build_prompt
from app.rag.retrievement import retrieve_documents
from Data.recommendation import recommend_technician


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    google_api_key=os.getenv("API_KEY"),
    temperature=0.3
)


def extract_text(response):

    content = response.content

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):

        text = ""

        for part in content:

            if isinstance(part, dict):
                text += part.get("text", "")

            elif hasattr(part, "text"):
                text += part.text

            else:
                text += str(part)

        return text.strip()

    return str(content)


def generate_response(history):

    history_text = "\n".join(
    f"{msg['role']}: {msg['content']}"
    for msg in history
)




    # -----------------------------
    # Clarification Stage
    # -----------------------------

    clarification = clarify_query(history_text)

    if clarification != "READY":
        return clarification

    # -----------------------------
    # Retrieval Stage
    # -----------------------------

    documents = retrieve_documents(history_text)

    if len(documents) == 0:

        return "عذرًا، لا أستطيع العثور على مشكلة مشابهة داخل قاعدة المعرفة."

    # -----------------------------
    # Generation Stage
    # -----------------------------

    prompt = build_prompt(history_text, documents)

    response = llm.invoke(prompt)

    answer = extract_text(response)

    # -----------------------------
    # Recommendation Stage
    # -----------------------------

    technician = recommend_technician(history_text)

    if technician:

        answer += f"""

-----------------------------------------

👨‍🔧 الفني المقترح

الاسم: {technician['name']}
التخصص: {technician['specialization']}
التقييم: ⭐ {technician['rating']}
الخبرة: {technician['experience']}
سعر الكشف: {technician['price']}
رقم الهاتف: {technician['phone']}

هل ترغب في حجز موعد مع هذا الفني؟
"""

    return answer