import os
import json
import re

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from app.rag.prompt import build_prompt
from app.rag.retrievement import retrieve_documents
from Data.recommendation import recommend_technician

load_dotenv()


 
llm = ChatOpenAI(
    model="gpt-4o-mini",          # or "gpt-4o" / "gpt-4.1-mini" depending on what you have access to
    api_key=os.getenv("API_KEY"),  # same OpenAI key used for Whisper in main.py
    temperature=0.3
)

#  get responce as son with 
# summary ----> summary for converstion
# answer ---->the output if found 
# follow_up ----> the question ai asks to make the problem more clear 
# ready_for_recommendation ----> true / recommend a worker or false/still asking
#  devic_type ---> for now the device and get the techniccan after that 
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
            "ready_for_recommendation": False, 
            "device_type" : None
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
            "technician": None, 
            "device_type": result.get("device_type")
        }

        # else return another question
        return {
            "summary": summary,
            "answer": "",                   # no responce 
            "follow_up": result["follow_up"],  # return question
            "technician": None,
             "device_type": result.get("device_type")  
        }

    # if no ore question so get the answer from vector db 
    documents = retrieve_documents(history_text)

    if not documents:
        return {
            "summary": summary,
            "answer": "عذرًا، لا أستطيع العثور على مشكلة مشابهة داخل قاعدة المعرفة.",
            "follow_up": None,
            "technician": None, 
            "device_type": result.get("device_type")
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
        "technician": technician,
        "device_type" : result.get("device_type")
    }