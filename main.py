<<<<<<< HEAD
from fastapi import FastAPI
from typing import Dict
from pydantic import BaseModel
from Data import technician
from app.rag.generation import generate_response
from Data.recommendation import recommend_technician


# save responce for all users str : user id , dic data (summary ,q_num ..)
sessions: Dict[str , Dict] = {}

class chatRequest(BaseModel):
    session_id: str 
    message: str


class chatResponce(BaseModel):
    session_id: str
    message: str
    follow_up: str 
    technicians : Dict 





# get top 5 
def get_technicians(query: str, top: int = 5):
    # retutn top 5
    return [
        {"name": "أحمد محمد", "specialization": "تبريد وتكييف", "rating": 4.9, "experience": "10 سنوات", "price": "200 جنيه", "phone": "01001234567"},
        {"name": "خالد علي", "specialization": "سباكة", "rating": 4.8, "experience": "8 سنوات", "price": "150 جنيه", "phone": "01007654321"},
        {"name": "سعيد حسن", "specialization": "كهرباء منزلية", "rating": 4.7, "experience": "7 سنوات", "price": "180 جنيه", "phone": "01005551234"},
        {"name": "محمود إبراهيم", "specialization": "صيانة أجهزة", "rating": 4.6, "experience": "6 سنوات", "price": "220 جنيه", "phone": "01009876543"},
        {"name": "ياسر عادل", "specialization": "نجارة", "rating": 4.5, "experience": "5 سنوات", "price": "170 جنيه", "phone": "01003456789"}
    ]




app = FastAPI(title=" الصنايعي الصح في الوقت الصح" ,
            description="هذا البوت يساعدك في تشخيص أعطال المنزل ويقترح لك فنيين محترفين.")
@app.get('/chat' )

async def root():
    return "hello"



@app.post('/chat',response_model=chatResponce)
async def fun(request : chatResponce):
    session_history = []
    session_summary = ""
    clarification_count = 0
    MAX_CLARIFICATIONS = 5


    #  if session is new
    if request.session_id not in sessions:
        sessions[request.session_id] = {
            "history": [],
            "summary": "",
            "clarification_count": 0
        }
        

     
    session = sessions[request.session_id]
   

    # add massage for user 
    session_history.append({"role": "user", "content": request.message})
    
    # generate responce 
    responce = generate_response(
        history=session_history,
        previous_summary=session_summary,
        clarification_count=clarification_count,
        max_clarifications=MAX_CLARIFICATIONS
    )
    
    # update summary
    session_summary = responce["summary"]
    
    # 
    assistant_reply = ""
    if responce["answer"]:
        assistant_reply += responce["answer"]

    
    if responce["follow_up"]:
        assistant_reply += f"\n\n❓ {responce['follow_up']}"
        clarification_count += 1  # increment the number of questions 
    else:
        clarification_count = 0   # reset to start count question num again



    technicians = []

    if responce["technician"]:
        tech = responce["technician"]
        assistant_reply += f"""
        

    👨‍🔧 الفني المقترح:
    الاسم: {tech.get('name', 'غير محدد')}
    التخصص: {tech.get('specialization', 'غير محدد')}
    التقييم: ⭐ {tech.get('rating', '0')}
    الخبرة: {tech.get('experience', 'غير محددة')}
    """
    
    # add chat anser to session history
    session_history.append({"role": "assistant", "content": assistant_reply})
    
 

    
    if responce.get("ready_for_recommendation") or responce["follow_up"] is None:
        history_text = ''

        for msg in session["history"]:
            history_text = "\n".join([f"{msg['role']}: {msg['content']}" ])
        technicians = get_technicians(history_text, limit=5)
        
        #  if technicains have been founded
        if technicians:
            assistant_reply += "\n\n👨‍🔧 **أفضل الفنيين المقترحين:**"
            for idx, tech in enumerate(technicians, 1):
                assistant_reply += f"""
                
                {idx}. الاسم: {tech.get('name', 'غير محدد')}
                التخصص: {tech.get('specialization', 'غير محدد')}
                التقييم: ⭐ {tech.get('rating', '0')}
            """
                
   
            # get chat responce
            return chatResponce(
                session_id=request.session_id,
                message=assistant_reply,
                follow_up=responce.get("follow_up"),
                technicians=technicians,
            )

            


# # # تشغيل الاختبار
# # if __name__ == "__main__":
# #     print("🚀 بدء اختبار بوت الصيانة...")
# #     print("اكتب 'خروج' للخروج.")
# #     while True:
# #         user_input = input("\n👤 أنت: ")
# #         if user_input.lower() == "خروج":
# #             break
# #         simulate_chat(user_input)
=======
from rag.prompt import build_prompt

# TODO: use build_prompt(query, docs) here
>>>>>>> origin/master
