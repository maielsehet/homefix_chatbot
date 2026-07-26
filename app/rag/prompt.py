from langchain_core.messages import SystemMessage, HumanMessage

def build_prompt(query, documents):
    context = "\n\n".join(
        doc.page_content if hasattr(doc, 'page_content') else str(doc)
        for doc in documents
    )

    system_prompt = (
        "أنت مساعد دعم فني لمنصة صيانة منزلية وخدمات فنيين. "
        "أجب على سؤال المستخدم بالاعتماد على السياق المُرفق (المشكلة، النوع، الحل)، "
        "حتى لو اختلفت صياغة السؤال قليلاً عن صياغة المشكلة في السياق، طالما أن المعنى العام قريب. "
        "إذا لم تجد في السياق أي مشكلة ذات صلة بسؤال المستخدم إطلاقًا، قل بالضبط: "
        "'عذرًا، لا يمكنني الإجابة بناءً على المستندات المتاحة.' "
        "أجب دائمًا باللغة العربية، بأسلوب واضح ومباشر."
    )

    human_prompt = f"""السياق:
{context}

السؤال:
{query}

الإجابة:"""

    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]