# from fastapi import FastAPI,UploadFile, File
# from typing import Dict, List, Optional
# from pydantic import BaseModel
# from Data import technician
# from app.rag.generation import generate_response
# from Data.recommendation import recommend_technician
# from Data.technician import *
# import sqlite3
# import tempfile
# import speech_recognition as sr
# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("API_KEY"))
# # recognizer = sr.Recognizer()
# # recognizer.energy_threshold = 300
# # recognizer.dynamic_energy_threshold = True

# # save responce for all users str : user id , dic data (summary ,q_num ..)
# sessions: Dict[str , Dict] = {}

# class chatRequest(BaseModel):
#     session_id: str 
#     message: str


# class chatResponce(BaseModel):
#     session_id: str
#     message: str
#     follow_up: Optional[str] = None     # if return none *at the end of chat since no question)
#     technicians : Optional[list[Dict]] = None 
#     device_type : Optional[str] = None




# # get top 5 
# def get_technicians(device_type: str, top: int = 5):
    
#     # retutn top 5
#     # #  create connection with db
#     # conn = sqlite3.connect("..db")
#     # #  cursor to excute query 
#     # cursor = conn.cursor()
#     # cursor.execute("select * from ..  order by rating des limit ?" , top)
#     # rows = cursor.fetchall()
#     # return [
#     #     {"name": row.name , "specialization": row.specialization , "rating": row.rating , "experience": row.experience}  for row in rows 
#     # ]

#     technicians = TECHNICIANS.get(device_type, [])
#     sorted_techs = sorted(technicians, key=lambda x: x.get('rating', 0), reverse=True)
#     return sorted_techs[:top]




# app = FastAPI(title=" الصنايعي الصح في الوقت الصح" ,
#             description="هذا البوت يساعدك في تشخيص أعطال المنزل ويقترح لك فنيين محترفين.")
# @app.get('/chat' )

# async def root():
#     return "hello"



# MAX_CLARIFICATIONS = 5

# @app.post('/chat',response_model=chatResponce)
# async def fun(request : chatRequest):
#     # session_history = []
#     # session_summary = ""
#     # clarification_count = 0


#     #  if session is new
#     if request.session_id not in sessions:
#         sessions[request.session_id] = {
#             "history": [],
#             "summary": "",
#             "clarification_count": 0
#         }
        

     
#     session = sessions[request.session_id]
   

#     # add massage for user 
#     session['history'].append({"role": "user", "content": request.message})
    
#     # generate responce 
#     responce = generate_response(
#         history=session['history'],
#         previous_summary=session['summary'],
#         clarification_count=session['clarification_count'],
#         max_clarifications=MAX_CLARIFICATIONS
#     )
    
#     # update summary
#     session['summary'] = responce["summary"]


#     assistant_reply = ""
#     if responce["answer"]:
#         assistant_reply += responce["answer"]

    
#     if responce["follow_up"]:
#         assistant_reply += f"\n\n❓ {responce['follow_up']}"
#         session["clarification_count"] += 1  # increment the number of questions 
#     else:
#         session["clarification_count"]  = 0   # reset to start count question num again



#     technicians = None

#     #  the converstion end and ready for recommend 
#     if responce.get("ready_for_recommendation") or responce["follow_up"] is None:
#         #  save history to send to worker 
#         history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in session["history"]])

#         #  get top 5 
#         device_type = responce.get("device_type")
#         if device_type:
#             technicians = get_technicians(device_type, top=5)
#         else:
#             technicians = []
#             assistant_reply += "\n\لم أتمكن من تحديد نوع الجهاز."





#         if technicians:
#             assistant_reply += "\n\n👨‍🔧 **أفضل الفنيين المقترحين:**"
#             for idx, tech in enumerate(technicians, 1):
#                 assistant_reply += f"""
                
#                 {idx}. الاسم: {tech.get('name', 'غير محدد')}
#                 التخصص: {tech.get('specialization', 'غير محدد')}
#                 التقييم: ⭐ {tech.get('rating', '0')}
#                 الخبرة: {tech.get('experience', 'غير محددة')}
#                 """
#         #  if not technichans 
#         else :
#             assistant_reply += "\n\n لا استطيع الوصول لصنايعى، يمكنك التوجه للصفحة الرئيسية."
    
     
#         #  save responce with technicains 
#         session["history"].append({"role": "assistant", "content": assistant_reply})
#         print(responce)



#     # get chat responce
#     return chatResponce(
#         session_id=request.session_id,
#         message=assistant_reply,
#         follow_up=responce.get("follow_up"),
#         technicians=technicians,
#         device_type=responce.get("device_type")
#     )

# @app.post("/voice")
# async def voice_chat(
#     session_id: str,
#     audio: UploadFile = File(...)
# ):

#     if session_id not in sessions:
#         sessions[session_id] = {
#             "history": [],
#             "summary": "",
#             "clarification_count": 0
#         }

#     session = sessions[session_id]

#     # Save uploaded audio temporarily
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
#         temp_audio.write(await audio.read())
#         temp_path = temp_audio.name

#     # Speech To Text

#     with open(temp_path, "rb") as audio_file:

#     transcript = client.audio.transcriptions.create(
#         model="whisper-1",
#         file=audio_file,
#         language="ar"
#     )

#     text = transcript.text

#     # Add user message
#     session["history"].append({
#         "role": "user",
#         "content": user_text
#     })

#     # Generate response
#     response = generate_response(
#         history=session["history"],
#         previous_summary=session["summary"],
#         clarification_count=session["clarification_count"]
#     )

#     session["summary"] = response.get(
#         "summary",
#         session["summary"]
#     )

#     if response["follow_up"]:
#         session["clarification_count"] += 1
#         bot_reply = response["follow_up"]
#     else:
#         session["clarification_count"] = 0
#         bot_reply = response["answer"]

#         if response["technician"]:
#             tech = response["technician"]

#             bot_reply += f"""

# الفني المقترح

# الاسم: {tech['name']}
# التخصص: {tech['specialization']}
# التقييم: ⭐ {tech['rating']}
# الخبرة: {tech['experience']}
# """

#     session["history"].append({
#         "role": "assistant",
#         "content": bot_reply
#     })

#     return {
#         "success": True,
#         "user_text": user_text,
#         "reply": bot_reply,
#         "follow_up": response["follow_up"] is not None
#     }


import os
from fastapi import FastAPI, UploadFile, File
from typing import Dict, List, Optional
from pydantic import BaseModel
from Data import technician
from app.rag.generation import generate_response
from Data.recommendation import recommend_technician
from Data.technician import *
import sqlite3
import tempfile
import subprocess
import speech_recognition as sr
from openai import OpenAI

client = OpenAI(api_key=os.getenv("API_KEY"))
# recognizer = sr.Recognizer()
# recognizer.energy_threshold = 300
# recognizer.dynamic_energy_threshold = True

# save responce for all users str : user id , dic data (summary ,q_num ..)
sessions: Dict[str, Dict] = {}


class chatRequest(BaseModel):
    session_id: str
    message: str


class chatResponce(BaseModel):
    session_id: str
    message: str
    follow_up: Optional[str] = None     # if return none *at the end of chat since no question)
    technicians: Optional[list[Dict]] = None
    device_type: Optional[str] = None


# get top 5
def get_technicians(device_type: str, top: int = 5):

    # retutn top 5
    # #  create connection with db
    # conn = sqlite3.connect("..db")
    # #  cursor to excute query
    # cursor = conn.cursor()
    # cursor.execute("select * from ..  order by rating des limit ?" , top)
    # rows = cursor.fetchall()
    # return [
    #     {"name": row.name , "specialization": row.specialization , "rating": row.rating , "experience": row.experience}  for row in rows
    # ]

    technicians = TECHNICIANS.get(device_type, [])
    sorted_techs = sorted(technicians, key=lambda x: x.get('rating', 0), reverse=True)
    return sorted_techs[:top]


app = FastAPI(
    title=" الصنايعي الصح في الوقت الصح",
    description="هذا البوت يساعدك في تشخيص أعطال المنزل ويقترح لك فنيين محترفين."
)


@app.get('/chat')
async def root():
    return "hello"


MAX_CLARIFICATIONS = 5


@app.post('/chat', response_model=chatResponce)
async def fun(request: chatRequest):
    # session_history = []
    # session_summary = ""
    # clarification_count = 0

    #  if session is new
    if request.session_id not in sessions:
        sessions[request.session_id] = {
            "history": [],
            "summary": "",
            "clarification_count": 0
        }

    session = sessions[request.session_id]

    # add massage for user
    session['history'].append({"role": "user", "content": request.message})

    # generate responce
    responce = generate_response(
        history=session['history'],
        previous_summary=session['summary'],
        clarification_count=session['clarification_count'],
        max_clarifications=MAX_CLARIFICATIONS
    )

    # update summary
    session['summary'] = responce["summary"]

    assistant_reply = ""
    if responce["answer"]:
        assistant_reply += responce["answer"]

    if responce["follow_up"]:
        assistant_reply += f"\n\n❓ {responce['follow_up']}"
        session["clarification_count"] += 1  # increment the number of questions
    else:
        session["clarification_count"] = 0   # reset to start count question num again

    technicians = None

    #  the converstion end and ready for recommend
    if responce.get("ready_for_recommendation") or responce["follow_up"] is None:
        #  save history to send to worker
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in session["history"]])

        #  get top 5
        device_type = responce.get("device_type")
        if device_type:
            technicians = get_technicians(device_type, top=5)
        else:
            technicians = []
            assistant_reply += "\n\nلم أتمكن من تحديد نوع الجهاز."

        if technicians:
            assistant_reply += "\n\n👨‍🔧 **أفضل الفنيين المقترحين:**"
            for idx, tech in enumerate(technicians, 1):
                assistant_reply += f"""

                {idx}. الاسم: {tech.get('name', 'غير محدد')}
                التخصص: {tech.get('specialization', 'غير محدد')}
                التقييم: ⭐ {tech.get('rating', '0')}
                الخبرة: {tech.get('experience', 'غير محددة')}
                """
        #  if not technichans
        else:
            assistant_reply += "\n\n لا استطيع الوصول لصنايعى، يمكنك التوجه للصفحة الرئيسية."

        #  save responce with technicains
        session["history"].append({"role": "assistant", "content": assistant_reply})
        print(responce)

    # get chat responce
    return chatResponce(
        session_id=request.session_id,
        message=assistant_reply,
        follow_up=responce.get("follow_up"),
        technicians=technicians,
        device_type=responce.get("device_type")
    )


@app.post("/voice")
async def voice_chat(
    session_id: str,
    audio: UploadFile = File(...)
):

    if session_id not in sessions:
        sessions[session_id] = {
            "history": [],
            "summary": "",
            "clarification_count": 0
        }

    session = sessions[session_id]

    # Debug: check what actually arrived
    print("filename:", audio.filename, "| content_type:", audio.content_type)

    # Save the raw upload first, whatever its real extension/container is
    raw_ext = os.path.splitext(audio.filename or "")[1] or ".bin"
    audio_bytes = await audio.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=raw_ext) as raw_audio:
        raw_audio.write(audio_bytes)
        raw_path = raw_audio.name

    print("saved raw upload to:", raw_path, "| size:", os.path.getsize(raw_path))

    if os.path.getsize(raw_path) == 0:
        os.remove(raw_path)
        return {
            "success": False,
            "error": "Uploaded audio file is empty."
        }

    # Some clients label files with an extension that doesn't match their
    # actual container/codec (e.g. a raw stream saved as ".m4a"), which makes
    # Whisper reject them with "Invalid file format" even though the
    # extension itself is supported. Re-encoding through ffmpeg into a clean
    # WAV file guarantees Whisper always receives a valid, recognizable file.
    wav_path = raw_path + "_converted.wav"
    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", raw_path, "-ar", "16000", "-ac", "1", wav_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0 or not os.path.exists(wav_path):
            print("ffmpeg error:", result.stderr)
            return {
                "success": False,
                "error": "Could not process the audio file. Make sure it is a valid audio recording and that ffmpeg is installed."
            }

        # Speech To Text
        with open(wav_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ar"
            )
    finally:
        for p in (raw_path, wav_path):
            if os.path.exists(p):
                os.remove(p)

    text = transcript.text
    user_text = text

    # Add user message
    session["history"].append({
        "role": "user",
        "content": user_text
    })

    # Generate response
    response = generate_response(
        history=session["history"],
        previous_summary=session["summary"],
        clarification_count=session["clarification_count"]
    )

    session["summary"] = response.get(
        "summary",
        session["summary"]
    )

    if response.get("follow_up"):
        session["clarification_count"] += 1
        bot_reply = response["follow_up"]
    else:
        session["clarification_count"] = 0
        bot_reply = response.get("answer", "")

        if response.get("technician"):
            tech = response["technician"]

            bot_reply += f"""

الفني المقترح

الاسم: {tech.get('name', 'غير محدد')}
التخصص: {tech.get('specialization', 'غير محدد')}
التقييم: ⭐ {tech.get('rating', '0')}
الخبرة: {tech.get('experience', 'غير محددة')}
"""

    session["history"].append({
        "role": "assistant",
        "content": bot_reply
    })

    return {
        "success": True,
        "user_text": user_text,
        "reply": bot_reply,
        "follow_up": response.get("follow_up") is not None
    }
