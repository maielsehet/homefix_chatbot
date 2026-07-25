
def build_prompt(query, documents):

    # Combine retrieved docs into a single context string
    context = "\n\n".join([doc.page_content if hasattr(doc, 'page_content') else str(doc) for doc in documents])
    
    # Define system instructions for the home maintenance chatbot
    system_prompt = (
        "You are a helpful customer support assistant for a home maintenance and handyman service platform. "
        "Answer the user's question using ONLY the provided context about services, prices, or fix instructions. "
        "If the answer is not in the context, say: 'Sorry, I cannot answer based on the available documents.'"
    )
    
    # Build the final prompt template
    prompt = f"""
System: {system_prompt}

Context:
{context}

Question:
{query}

Answer:
                """
    return prompt.strip() 