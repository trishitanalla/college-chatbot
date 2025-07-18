from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from llama_query import generate_answer
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")
CORS(app)

# Configuration
EMBED_MODEL = os.getenv("EMBED_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
DB_PATH = os.getenv("VECTOR_DB_PATH", "vectorstore.faiss")

# Load FAISS vector database
try:
    vectordb = FAISS.load_local(
        DB_PATH,
        HuggingFaceEmbeddings(model_name=EMBED_MODEL),
        allow_dangerous_deserialization=True
    )
except Exception as e:
    print("❌ Failed to load FAISS vector store:", e)
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
            return jsonify({"error": "Vector store not loaded"}), 500

        # Retrieve similar documents
        docs = vectordb.similarity_search(q, k=5)

        # Generate answer
        answer = generate_answer(q, docs)

        return jsonify({
            "answer": answer,
            "sources": [d.metadata for d in docs]
        })

    except Exception as e:
        print("🔥 Backend error:", e)
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

# Serve React frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    return send_from_directory(app.static_folder, "index.html")

# Entry point
if __name__ == "__main__":
    app.run(port=5000, debug=True)
