import json
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = "vectorstore.faiss"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def ingest():
    with open("scraped.json", "r", encoding="utf-8") as f:
        pages = json.load(f)

    docs = []
    for page in pages:
        docs.append(Document(page_content=page["text"], metadata={"source": page["url"]}))

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectordb = FAISS.from_documents(docs, embeddings)
    vectordb.save_local(DB_PATH)
    print(f"Saved vectorstore with {len(docs)} documents at '{DB_PATH}'")

if __name__ == "__main__":
    ingest()
