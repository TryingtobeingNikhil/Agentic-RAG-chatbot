# Adaptive RAG — Agentic AI Chatbot....

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.5.4-orange.svg)](https://python.langchain.com/langgraph/)
[![Free to Run](https://img.shields.io/badge/Cost-Free-brightgreen.svg)](#-cost)

## 📋 Overview

Adaptive RAG is an intelligent end-to-end Retrieval-Augmented Generation system powered by agentic AI architecture. It combines dynamic query routing, intelligent document retrieval, and advanced LLM capabilities to provide accurate, context-aware answers to user queries.

The system intelligently adapts its retrieval strategy based on query type — using indexed documents, general knowledge, or real-time web search to generate comprehensive responses. Built with a modular architecture using LangGraph for workflow orchestration and FAISS for local vector storage.

---

## 🎯 Key Features

- **Intelligent query routing**: index, general knowledge, or web search
- **Document processing** with intelligent chunking and embedding
- **Relevance grading** and automatic query rewriting
- **Multi-agent ReAct architecture** for reasoning and acting
- **Optional MongoDB** chat history with automatic in-memory fallback
- **Streamlit web interface** with PDF and TXT document upload
- **FastAPI backend** with async REST endpoints

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Streamlit Web Application                               │  │
│  │  • Chat Interface                                        │  │
│  │  • Document Upload (PDF, TXT)                            │  │
│  │  • Session Management                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                       FastAPI Backend                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  REST API Endpoints                                      │  │
│  │  • POST /rag/query                                       │  │
│  │  • POST /rag/documents/upload                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph Orchestration                      │
│  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐         │
│  │ Query   │→ │ Classify │→ │ Router  │→ │ Pipeline │         │
│  │ Analyze │  │ Query    │  │ Output  │  │ Exec     │         │
│  └─────────┘  └──────────┘  └─────────┘  └──────────┘         │
└─────────────────────────────────────────────────────────────────┘
                            ↓
        ┌──────────────────┬──────────────────┬────────────────┐
        ↓                  ↓                  ↓                ↓
   ┌─────────┐       ┌──────────┐      ┌────────────┐   ┌──────────┐
   │Retriever│       │ General  │      │ Web Search │   │ Response │
   │ (FAISS) │       │   LLM    │      │  (Tavily)  │   │Generator │
   └─────────┘       └──────────┘      └────────────┘   └──────────┘
        ↓                  ↓                  ↓                ↓
        └──────────────────┬──────────────────┬────────────────┘
                           ↓
            ┌─────────────────────────────────┐
            │        Response to User          │
            └─────────────────────────────────┘
```

### Graph Nodes

1. **query_analysis** — Classifies incoming queries as `index`, `general`, or `search`
2. **retriever** — ReAct agent retrieves relevant documents from FAISS
3. **grade** — Evaluates relevance of retrieved documents
4. **rewrite** — Optimises query for better retrieval results
5. **generate** — Generates final response from context
6. **web_search** — Performs real-time web search via Tavily
7. **general_llm** — Answers from Groq LLM general knowledge

---

## 📦 Project Structure

```
my-adaptive-rag/
├── src/                              # Main source code
│   ├── main.py                       # FastAPI application entry point
│   ├── api/                          # API routes and endpoints
│   │   └── routes.py                 # RAG query and document upload endpoints
│   ├── config/                       # Configuration management
│   │   ├── settings.py               # Application settings (Groq, HuggingFace, etc.)
│   │   └── prompts.yaml              # LLM prompts and system messages
│   ├── core/                         # Core utilities
│   │   ├── config.py                 # Core configuration + env loading
│   │   └── logger.py                 # Logging setup
│   ├── db/                           # Database layer
│   │   └── mongo_client.py           # Optional MongoDB client (falls back to memory)
│   ├── llms/                         # Language model integrations
│   │   └── groq_llm.py               # Groq llama3-70b-8192 (free)
│   ├── memory/                       # Chat memory management
│   │   ├── chat_history_mongo.py     # MongoDB-backed chat history (auto fallback)
│   │   └── chathistory_in_memory.py  # In-memory chat history
│   ├── models/                       # Data models and schemas
│   │   ├── state.py                  # Graph state definition
│   │   ├── query_request.py          # Query request schema
│   │   ├── grade.py                  # Relevance grade model
│   │   ├── route_identifier.py       # Route classification model
│   │   └── verification_result.py    # Answer verification model
│   ├── rag/                          # RAG pipeline implementation
│   │   ├── graph_builder.py          # LangGraph workflow construction
│   │   ├── nodes.py                  # Graph node placeholder
│   │   ├── retriever_setup.py        # FAISS vector store + HuggingFace embeddings
│   │   ├── document_upload.py        # Document processing and upload
│   │   └── reAct_agent.py            # ReAct agent setup
│   └── tools/                        # Utility tools and functions
│       ├── common_tools.py           # Shared utility functions
│       └── graph_tools.py            # Graph routing and decision tools
│
├── streamlit_app/                    # Streamlit web application
│   ├── home.py                       # Authentication and login page
│   ├── pages/                        # Multi-page application
│   │   └── chat.py                   # Chat interface and document upload
│   └── utils/                        # Streamlit utilities
│       └── api_client.py             # Backend API client
│
├── .env.example                      # Environment variable template
├── .gitignore                        # Git ignore rules
├── README.md                         # This file
└── requirements.txt                  # Python dependencies
```

---

## 💸 Cost

**This project is completely free to run.**

| Service | Cost | Notes |
|---|---|---|
| **Groq API** | Free | Generous free tier — [console.groq.com](https://console.groq.com) |
| **HuggingFace Embeddings** | Free | Runs fully locally, no API key needed |
| **FAISS** | Free | Runs fully locally, no account needed |
| **MongoDB** | Free / Optional | App works without it — uses in-memory fallback |
| **Tavily Search** | Free tier | 1,000 requests/month — [app.tavily.com](https://app.tavily.com) |

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000
```

### 1. Query Endpoint
**Process a RAG query and get an intelligent response**

```http
POST /rag/query
Content-Type: application/json

{
  "query": "What is the main topic of the document?",
  "session_id": "user_session_123"
}
```

**Response:**
```json
{
  "result": {
    "type": "ai",
    "content": "Based on the document, the main topic is..."
  }
}
```

**Parameters:**
- `query` (string, required): User's question or query
- `session_id` (string, required): Unique session identifier for conversation tracking

**Status Codes:** `200` Success · `400` Invalid request · `500` Server error

---

### 2. Document Upload Endpoint
**Upload documents for RAG indexing**

```http
POST /rag/documents/upload
X-Description: Brief description of the document

Form Data:
- file: <PDF or TXT file>
```

**Response:**
```json
{
  "status": true
}
```

**Supported formats:** PDF (`.pdf`), Plain Text (`.txt`)

**Status Codes:** `200` Uploaded · `400` Invalid file type · `500` Processing error

---

## 📖 Setup & Usage

### Prerequisites

- Python 3.9 or higher
- Groq API key — **free** at [console.groq.com](https://console.groq.com)
- Tavily API key — **free** at [app.tavily.com](https://app.tavily.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/TryingtobeingNikhil/Agentic-RAG-chatbot.git
cd Agentic-RAG-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

```bash
cp .env.example .env
# Open .env and fill in your GROQ_API_KEY and TAVILY_API_KEY
```

### Running the App

```bash
# Terminal 1 — Start FastAPI backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 — Start Streamlit frontend
streamlit run streamlit_app/home.py

# Access:
# Web UI   → http://localhost:8501
# API docs → http://localhost:8000/docs
```

---

## 🧪 Example Usage

**Using cURL:**
```bash
# Upload a document
curl -X POST http://localhost:8000/rag/documents/upload \
  -H "X-Description: Sample document about Python" \
  -F "file=@document.pdf"

# Query the RAG system
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Tell me about Python",
    "session_id": "user_123"
  }'
```

**Using Python:**
```python
import requests

# Query endpoint
response = requests.post(
    "http://localhost:8000/rag/query",
    json={
        "query": "What is Python?",
        "session_id": "user_123"
    }
)
print(response.json())
```

---

## 📚 Technology Stack

| Component | Technology |
|---|---|
| **LLM** | Groq llama3-70b-8192 — Free |
| **Embeddings** | HuggingFace all-MiniLM-L6-v2 — Free, Local |
| **Workflow** | LangGraph |
| **LLM Framework** | LangChain |
| **API Backend** | FastAPI + Uvicorn |
| **Frontend** | Streamlit |
| **Vector DB** | FAISS — Free, Local |
| **Chat History** | In-Memory (MongoDB optional) |
| **Web Search** | Tavily |
| **Validation** | Pydantic |

---

## 🔐 Security

- Store all API keys in `.env` file, **never commit it**
- `.env` is already included in `.gitignore`
- Use HTTPS in production
- Implement rate limiting for public deployments

---

## 🚀 Deployment

```bash
# Development
python -m uvicorn src.main:app --reload

# Production
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 👤 Author

**Nikhil Mourya**
- GitHub: [@TryingtobeingNikhil](https://github.com/TryingtobeingNikhil)
- Project: [Agentic-RAG-chatbot](https://github.com/TryingtobeingNikhil/Agentic-RAG-chatbot)

---

## 📄 License

MIT License
