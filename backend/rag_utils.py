# rag_utils.py

from llama_query import query_llm

def generate_answer(prompt, retrieved_docs, max_tokens=512, temperature=0.1):
    context = "\n\n".join(
        [f"[{doc.metadata.get('source', 'unknown')}]:\n{doc.page_content}" for doc in retrieved_docs]
    )
    full_prompt = f"{context}\n\nUser: {prompt}\nAssistant:"

    # Call your LLM wrapper
    answer = query_llm(full_prompt, max_tokens=max_tokens, temperature=temperature)
    return answer
