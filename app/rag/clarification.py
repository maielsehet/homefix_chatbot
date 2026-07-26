from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    google_api_key=os.getenv("API_KEY"),
    temperature=0
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


def clarify_query(history):

    prompt = [

        SystemMessage(
            content="""
أنت موظف خدمة عملاء في HomeFix.

ستقرأ المحادثة كاملة.

إذا أصبحت المعلومات كافية للبحث داخل قاعدة المعرفة
فأجب بكلمة واحدة فقط

READY

بدون أي كلام آخر.

إذا كانت المعلومات ناقصة

اسأل سؤالاً واحداً فقط.

لا تكرر سؤالاً تمت الإجابة عنه.

رتب الأسئلة بهذا الترتيب:

1- نوع الجهاز
2- الماركة
3- وصف المشكلة بالتحديد
4- تفاصيل إضافية إن احتجت

لا تعط حلولاً.

لا تشرح.

أجب بالعربية فقط.
"""
        ),

        HumanMessage(content=history)

    ]

    response = llm.invoke(prompt)

    return extract_text(response)