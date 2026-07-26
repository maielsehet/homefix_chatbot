from langchain_core.messages import SystemMessage, HumanMessage

def build_prompt(query, documents):

    context = "\n\n".join(
        doc.page_content if hasattr(doc, "page_content") else str(doc)
        for doc in documents
    )

    system_prompt = """
أنت مساعد دعم فني لمنصة HomeFix.

ستحصل على:
1. سؤال المستخدم.
2. مجموعة من المستندات المسترجعة من قاعدة المعرفة.

قواعد الإجابة:

1. أجب اعتمادًا على المستندات فقط.
2. لا تستخدم أي معلومة غير موجودة في المستندات.
3. لا تخمن أي معلومة.
4. إذا كانت هناك عدة مستندات، اختر المستند الأكثر ارتباطًا بسؤال المستخدم.
5. لا تدمج حلولًا تخص موديلات أو أجهزة مختلفة.
6. إذا لم تجد مستندًا مناسبًا، فأجب فقط:
"عذرًا، لا يمكنني الإجابة بناءً على المستندات المتاحة."
7. إذا كان الحل عبارة عن خطوات، اعرضها في نقاط مرتبة.
8. أجب باللغة العربية الواضحة.
"""

    human_prompt = f"""
المستندات:

{context}

==========================

سؤال المستخدم:

{query}

الإجابة:
"""

    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]