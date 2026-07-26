from langchain_core.messages import SystemMessage, HumanMessage


def build_prompt(history, documents):

    context = "\n\n".join(

        doc.page_content

        for doc in documents

    )

    system_prompt = """
أنت فني دعم لمنصة HomeFix.

اعتمد فقط على المعلومات الموجودة داخل السياق.

قواعد مهمة:

1- لا تؤلف أي معلومات.

2- إذا لم تجد الحل داخل السياق قل:

عذرًا، لا أستطيع العثور على حل داخل قاعدة المعرفة.

3- إذا وُجد أكثر من مستند متشابه:

اختر الحل الأكثر تطابقًا مع المشكلة.

ولا تعرض كل الحلول.

4- لا تعرض خطوات ليست موجودة داخل المستند.

5- أجب بالعربية.

6- لا تذكر كلمة "السياق".

7- لا تذكر أنك AI.

8- اجعل الإجابة مختصرة وواضحة.
"""

    human_prompt = f"""
المحادثة:

{history}

-----------------------

السياق:

{context}

-----------------------

الإجابة:
"""

    return [

        SystemMessage(content=system_prompt),

        HumanMessage(content=human_prompt)

    ]