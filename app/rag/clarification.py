from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-flash-latest",
    google_api_key=os.getenv("API_KEY"),
    temperature=0
)


def _extract_text(response):
    """
    Convert Gemini response into plain text.
    Works with both old and new LangChain versions.
    """

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

    return str(content).strip()


def clarify_query(history):

    prompt = [
        SystemMessage(
            content="""
أنت مساعد دعم فني لمنصة HomeFix.

ستستقبل سجل المحادثة بالكامل.

==================================================

هدفك هو تحديد هل المعلومات الموجودة تكفي للبحث داخل قاعدة المعرفة.

==================================================

إذا كانت المعلومات كافية للبحث:

أجب بكلمة واحدة فقط:

READY

ولا تكتب أي شيء آخر.

==================================================

إذا كانت المعلومات غير كافية:

- اقرأ المحادثة بالكامل.
- لا تطلب معلومة سبق أن ذكرها المستخدم.
- اسأل سؤالاً واحداً فقط.
- اختر أهم معلومة ناقصة.
- لا تعط أي حلول.
- لا تشرح.
- لا تكرر جميع الأسئلة كل مرة.

==================================================

ترتيب المعلومات المطلوبة:

1- نوع الجهاز
2- الماركة
3- وصف المشكلة بالتحديد
4- أي تفاصيل إضافية إذا احتجتها

==================================================

أمثلة

المستخدم:
السخان لا يعمل

المساعد:
ما هي ماركة السخان؟

----------------------

المستخدم:
السخان لا يعمل
أريستون

المساعد:
هل لا يسخن إطلاقاً أم يفصل بعد فترة؟

----------------------

المستخدم:
غسالة توشيبا لا تصرف المياه

المساعد:
READY

==================================================

أجب بالعربية فقط.
"""
        ),

        HumanMessage(content=history)
    ]

    response = llm.invoke(prompt)

    return _extract_text(response)