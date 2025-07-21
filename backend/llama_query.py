# llama_query.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/api/generate")
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "mistral:7b") # <-- FIX: Use model from .env

def query_llm(prompt, temperature=0.1):
    """
    Query the locally running Ollama model.
    """
    payload = {
        "model": LLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    try:
        response = requests.post(LLM_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        return data.get("response", "").strip()
    except requests.exceptions.RequestException as e:
        print(f"🔥 Error querying Ollama: {e}")
        # Return a user-friendly error message
        return "Sorry, I'm having trouble connecting to the language model. Please ensure Ollama is running."


def generate_answer(question, retrieved_docs):
    """
    Composes a detailed prompt with context and instructions, then queries the LLM.
    """
    # Create the context string from the retrieved documents
    context = "\n\n---\n\n".join([
        f"Source URL: {d.metadata.get('source', 'unknown')}\nContent: {d.page_content}"
        for d in retrieved_docs
    ])

    # Improved prompt template
    prompt_template = f"""
You are a helpful assistant for the Sri Vasavi Engineering College. Your task is to answer user questions based ONLY on the provided context from the college website.

Do not use any external knowledge. If the information is not in the context, you must say "I do not have enough information from the website to answer that question."

Here is the relevant context scraped from the website:
---
{context}
---

Based on the context above, please answer the following question.

User Question: {question}

Assistant's Answer:
"""

    return query_llm(prompt_template)