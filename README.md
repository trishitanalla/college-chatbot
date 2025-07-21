# 🎓 College Chatbot Assistant (Under Development)

This is a **college website chatbot** project currently under development. It is designed to assist users by answering queries related to the college using a Retrieval-Augmented Generation (RAG) approach powered by LLMs.

## 🚧 Status
**🔧 This project is still in progress. Expect frequent updates and improvements.**

---

## 💡 Project Overview

The goal of this chatbot is to:
- Provide quick answers to queries about the college (departments, courses, admissions, events, etc.)
- Use a Large Language Model (LLM) with RAG for accurate and contextual responses
- Serve as an interactive assistant directly on the college website

---

## 🛠️ Tech Stack

- **Web Scraping**: BeautifulSoup / Custom Crawler
- **Data Chunking**: LangChain
- **Embeddings**: `mxbai-embed-large`
- **Vector Database**: FAISS / Chroma
- **LLM Backend**: LLaMA / Gemini via Ollama
- **API**: Python + Flask
- **Frontend**: HTML / React (TBD)

---

## 📂 Project Structure

college-chatbot/
├── backend/
│ ├── embed_chunks.py
│ ├── query_engine.py
│ └── app.py
├── frontend/
│ ├── index.html
│ └── chatbot.js
├── vector_db/
│ └── faiss_index/
├── scraped_data/
│ └── website_content.json
└── README.md

# 🤖 College Chatbot Assistant - How to Run

This is a RAG-based chatbot designed to answer queries using content from the college website.

## 📦 Prerequisites

- Python 3.10+
- Node.js + npm
- Ollama (for running local LLM like LLaMA/Gemini)

---

## 🛠 Setup Instructions

### ✅ 1. Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
# Scrape content from college website
python scrapper.py

# Generate embeddings from scraped data
python ingest.py
python app.py


cd frontend
npm install
npm run dev
