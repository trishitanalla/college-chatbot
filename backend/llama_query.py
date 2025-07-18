import requests
import os

# Correct endpoint for Ollama
LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/api/generate")

def query_llm(prompt, max_tokens=512, temperature=0.1):
    """
    Query Ollama model running locally (e.g., qwen:14b).
    """
    payload = {
        "model": "qwen:14b",          # Make sure this model is pulled with `ollama pull qwen:14b`
        "prompt": prompt,
        "stream": False,
        "temperature": temperature
    }

    response = requests.post(LLM_API_URL, json=payload)
    response.raise_for_status()

    data = response.json()

    # Ollama responds with {"response": "your text"} not {"text": ...}
    return data.get("response", "").strip()

def generate_answer(prompt, retrieved_docs):
    """
    Compose the prompt with context from retrieved documents and get the answer.
    """
    context = "\n\n".join([
        f"[{d.metadata.get('source', 'unknown')}]:\n{d.page_content}"
        for d in retrieved_docs
    ])

    full_prompt = f"{context}\n\nUser: {prompt}\nAssistant:"
    return query_llm(full_prompt)
