# # from app.rag.retrievement import retrieve_documents
# # from app.rag.prompt import build_prompt
# # from app.rag.clarification import clarify_query
# # from langchain_google_genai import ChatGoogleGenerativeAI
# # from dotenv import load_dotenv
# # import os

# # load_dotenv()

# # llm = ChatGoogleGenerativeAI(
# #     model="models/gemini-flash-latest",
# #     google_api_key=os.getenv("API_KEY"),
# #     temperature=0.3
# # )

# # def extract_text(response):

# #     content = response.content

# #     if isinstance(content, str):
# #         return content.strip()

# #     if isinstance(content, list):

# #         text = ""

# #         for part in content:

# #             if isinstance(part, dict):
# #                 text += part.get("text", "")

# #             elif hasattr(part, "text"):
# #                 text += part.text

# #             else:
# #                 text += str(part)

# #         return text.strip()

# #     return str(content).strip()

# # def generate_response(conversation_history):

   
# #     last_query = conversation_history[-1]["content"]

    
# #     history_text = ""

# #     for message in conversation_history:
# #         history_text += f"{message['role']}: {message['content']}\n"

# #     clarification = clarify_query(history_text)

# #     if clarification != "READY":
# #         return clarification

# #     docs = retrieve_documents(history_text)

# #     prompt = build_prompt(history_text, docs)

# #     response = llm.invoke(prompt)
    

# #     return extract_text(response)



# import os
# from dotenv import load_dotenv

# from langchain_google_genai import ChatGoogleGenerativeAI

# from app.rag.clarification import clarify_query
# from app.rag.prompt import build_prompt
# from app.rag.retrievement import retrieve_documents
# from Data.recommendation import recommend_technician


# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="models/gemini-2.5-flash",
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

#     return str(content)


# def generate_response(history):

#     history_text = "\n".join(
#     f"{msg['role']}: {msg['content']}"
#     for msg in history
# )




#     # -----------------------------
#     # Clarification Stage
#     # -----------------------------

#     clarification = clarify_query(history_text)

#     if clarification != "READY":
#         return clarification

#     # -----------------------------
#     # Retrieval Stage
#     # -----------------------------

#     documents = retrieve_documents(history_text)

#     if len(documents) == 0:

#         return "عذرًا، لا أستطيع العثور على مشكلة مشابهة داخل قاعدة المعرفة."

#     # -----------------------------
#     # Generation Stage
#     # -----------------------------

#     prompt = build_prompt(history_text, documents)

#     response = llm.invoke(prompt)

#     answer = extract_text(response)

#     # -----------------------------
#     # Recommendation Stage
#     # -----------------------------

#     technician = recommend_technician(history_text)

#     if technician:

#         answer += f"""

# -----------------------------------------

# 👨‍🔧 الفني المقترح

# الاسم: {technician['name']}
# التخصص: {technician['specialization']}
# التقييم: ⭐ {technician['rating']}
# الخبرة: {technician['experience']}
# هل ترغب في حجز موعد مع هذا الفني؟
# """

#     return answer
# # سعر الكشف: {technician['price']}
# # رقم الهاتف: {technician['phone']}







import os
import json
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.rag.prompt import build_prompt
from app.rag.retrievement import retrieve_documents
from Data.recommendation import recommend_technician

load_dotenv()

llm = ChatGoogleGenerativeAI(
    # model="models/gemini-2.5-flash",
    model="gemini-3.6-flash",
    google_api_key=os.getenv("API_KEY"),
    temperature=0.3
)

#  get responce as son with 
# summary ----> summary for converstion
# answer ---->the output if found 
# follow_up ----> the question ai asks to make the problem more clear 
# ready_for_recommendation ----> true / recommend a worker or false/still asking
def get_response(prompt):

    response = llm.invoke(prompt)
    text = response.content

    if not isinstance(text, str):
        new_text = ""
        for part in text:
            if isinstance(part, dict):
                var = part.get("text", "")
            else:
                var = getattr(part, "text", str(part))   
            new_text += var

        text = new_text
        

    try:
        return json.loads(text)

    except:
        # extract json part 
        #  DOT ALL match for all lines not only the first one
        match = re.search(r"\{.*\}", text, re.DOTALL)

        #  if found take it using .group
        if match:
            return json.loads(match.group())

        return {
            "summary": "",
            "answer": "",
            "follow_up": None,
            "ready_for_recommendation": False
        }



# max_clarifications ---> the max question chat can ask (to save tokens also)
def generate_response(history, previous_summary="" , clarification_count=0 , max_clarifications=5):

    history_text = "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in history
    )

    # prevous response
    result = get_response(build_prompt(history_text))
    #  summary for the current conversation 
    summary = result.get("summary", previous_summary)



    #  chat ask a question
    if result.get("follow_up"):
        if clarification_count >= max_clarifications:
            return {
            "summary": summary,
            "answer": "آسف، وصلنا للحد الأقصى من الأسئلة. أنصحك بالتواصل مع الدعم الفني مباشرة للحصول على مساعدة دقيقة.",
            "follow_up": None,   # stop question (ai stopped ask more )
            "technician": None
        }

        # else return another question
        return {
            "summary": summary,
            "answer": "",                   # no responce 
            "follow_up": result["follow_up"],  # return question
            "technician": None
        }

    # if no ore question so get the answer from vector db 
    documents = retrieve_documents(history_text)

    if not documents:
        return {
            "summary": summary,
            "answer": "عذرًا، لا أستطيع العثور على مشكلة مشابهة داخل قاعدة المعرفة.",
            "follow_up": None,
            "technician": None
        }


    # recommend a technician
    result = get_response(build_prompt(history_text, documents))

    technician = None

    if result.get("ready_for_recommendation"):
        technician = recommend_technician(history_text)

    return {
        "summary": result.get("summary", summary),
        "answer": result.get("answer", ""),
        "follow_up": None,
        "technician": technician
    }