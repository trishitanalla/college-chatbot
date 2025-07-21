# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from llama_query import generate_answer  # <-- Ensure this is the only import for generation
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")
CORS(app)

# Configuration from environment variables
EMBED_MODEL = os.getenv("EMBED_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
DB_PATH = os.getenv("VECTOR_DB_PATH", "vectorstore.faiss")

# Load FAISS vector database
print("Loading vector database...")
try:
    vectordb = FAISS.load_local(
        DB_PATH,
        HuggingFaceEmbeddings(model_name=EMBED_MODEL),
        allow_dangerous_deserialization=True
    )
    print("✅ Vector database loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load FAISS vector store: {e}")
    vectordb = None  # Fail-safe if loading fails

# Route for question-answering
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        q = data.get("question") if data else None

        if not q:
            return jsonify({"error": "No question provided"}), 400

        if vectordb is None:
            return jsonify({"error": "Vector store not loaded. Please check backend logs."}), 500

        # Retrieve similar documents
        print(f"Searching for documents related to: '{q}'")
        docs = vectordb.similarity_search(q, k=5) # k=5 means we retrieve top 5 chunks

        # Generate answer
        print("Generating answer...")
        answer = generate_answer(q, docs)
        print("Answer generated.")

        return jsonify({
            "answer": answer,
            "sources": [d.metadata for d in docs]
        })

    except Exception as e:
        print(f"🔥 Backend error: {e}")
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

# Serve React frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# Entry point
if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=False)