from app.rag.generation import generate_response

# هذه محاكاة للجلسة (سنخزن التاريخ والملخص والعداد)
session_history = []
session_summary = ""
clarification_count = 0
MAX_CLARIFICATIONS = 5

def simulate_chat(user_input):
    global session_history, session_summary, clarification_count
    
    # 1. أضف رسالة المستخدم
    session_history.append({"role": "user", "content": user_input})
    
    # 2. استدعِ البوت مع تمرير العداد
    result = generate_response(
        history=session_history,
        previous_summary=session_summary,
        clarification_count=clarification_count,
        max_clarifications=MAX_CLARIFICATIONS
    )
    
    # 3. حدّث الملخص والعداد
    session_summary = result["summary"]
    
    # 4. ابنِ الرد الذي سيراه المستخدم
    assistant_reply = ""
    if result["answer"]:
        assistant_reply += result["answer"]
    
    if result["follow_up"]:
        assistant_reply += f"\n\n❓ {result['follow_up']}"
        clarification_count += 1  # زود العداد لأنه سأل سؤالاً
    else:
        clarification_count = 0   # أعد التعيين لأنه أجاب نهائياً
    
    if result["technician"]:
        tech = result["technician"]
        assistant_reply += f"""
        
👨‍🔧 الفني المقترح:
الاسم: {tech.get('name', 'غير محدد')}
التخصص: {tech.get('specialization', 'غير محدد')}
التقييم: ⭐ {tech.get('rating', '0')}
الخبرة: {tech.get('experience', 'غير محددة')}
# سعر الكشف: {tech.get('price', 'غير محدد')}
# رقم الهاتف: {tech.get('phone', 'غير متاح')}
"""
    
    # 5. أضف رد المساعد للتاريخ (للسياق)
    session_history.append({"role": "assistant", "content": assistant_reply})
    
    # 6. اطبع النتيجة
    print(f"\n🤖 المساعد: {assistant_reply}")
    print(f"📝 الملخص الحالي: {session_summary}")
    print(f"🔢 عدد الأسئلة المطروحة: {clarification_count}")
    print("-" * 60)
    return result

# تشغيل الاختبار
if __name__ == "__main__":
    print("🚀 بدء اختبار بوت الصيانة...")
    print("اكتب 'exit' للخروج.")
    while True:
        user_input = input("\n👤 أنت: ")
        if user_input.lower() == "exit":
            break
        simulate_chat(user_input)