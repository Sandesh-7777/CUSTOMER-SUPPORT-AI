# Multi-Agent AI Customer Support

A full-stack AI customer support chatbot for **TechMart Electronics** — a fictional consumer electronics company. Customer queries are automatically classified by intent and routed to one of five specialized AI agents, each grounded in real company documents via RAG (Retrieval-Augmented Generation).

**Live demo:** `[https://customer-support-ai-ashy.vercel.app)`  
**Backend API:** `[https://customer-support-ai-backend-euiq.onrender.com)`

---

## What it does

When a user sends a message, the system:

1. **Detects intent** — classifies the query as billing, technical, product, complaint, or FAQ
2. **Routes to a specialist** — one of five purpose-built agents handles the query
3. **Retrieves context** — searches a local vector database built from company PDFs
4. **Answers from documents** — the LLM responds using retrieved context, not guesswork
5. **Persists history** — conversation history is saved per user in MongoDB

---

## Tech stack

| Layer | Technology | Notes |
|---|---|---|
| LLM | Groq (`openai/gpt-oss-20b`) | Free tier — fast inference |
| Embeddings | ChromaDB default (ONNX) | Runs locally, no API key needed |
| Vector DB | ChromaDB | Local persistent store |
| Backend | FastAPI + uvicorn | Python REST API |
| Database | MongoDB Atlas | Free 512MB tier |
| Frontend | Next.js + Tailwind CSS | React, App Router |
| Auth | JWT + bcrypt | Signup/login, no third-party service |
| Hosting | Render (backend) + Vercel (frontend) | Both free tiers |

---

## Project structure

```
customer-support-ai/
├── backend/
│   ├── main.py                  # FastAPI app, all routes
│   ├── auth.py                  # JWT + bcrypt password hashing
│   ├── requirements.txt
│   ├── start.sh                 # Render startup script
│   ├── agents/
│   │   ├── router.py            # Intent detection
│   │   ├── billing.py
│   │   ├── technical.py
│   │   ├── product.py
│   │   ├── complaint.py
│   │   └── faq.py
│   └── rag/
│       ├── ingest.py            # PDF → chunks → embeddings → ChromaDB
│       ├── retriever.py         # Semantic search over ChromaDB
│       └── vectorstore/         # Pre-built ChromaDB index (committed)
├── frontend/
│   └── src/
│       ├── app/
│       │   └── page.jsx         # Entry point — shows auth or chat
│       ├── components/
│       │   ├── AuthForm.jsx     # Login / signup form
│       │   ├── ChatInterface.jsx
│       │   ├── Message.jsx      # Renders Markdown, tables, agent badge
│       │   └── InputBar.jsx
│       ├── context/
│       │   └── AuthContext.jsx  # Auth state across the app
│       └── services/
│           └── api.js           # All fetch() calls to backend
└── knowledge_base/
    ├── FAQ.pdf
    ├── RefundPolicy.pdf
    ├── ShippingPolicy.pdf
    ├── Pricing.pdf
    ├── Warranty.pdf
    └── TechSupport.pdf
```

---

## Local setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- A free [Groq API key](https://console.groq.com)
- A free [MongoDB Atlas](https://mongodb.com/atlas) cluster

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/customer-support-ai.git
cd customer-support-ai
```

### 2. Backend setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip3 install -r requirements.txt

# Also install these locally (only needed for PDF ingestion, not on server)
pip3 install pypdf langchain langchain-community sentence-transformers fpdf2
```

Create `backend/.env`:

```
GROQ_API_KEY=your_groq_key_here
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/support_ai?retryWrites=true&w=majority
JWT_SECRET=your_random_secret_here
```

Generate a JWT secret:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**Mac users (Python 3.13) — fix SSL certificates once:**
```bash
open /Applications/Python\ 3.13/Install\ Certificates.command
```

### 3. Generate knowledge base PDFs

```bash
cd backend
python3 create_knowledge_base.py
```

This creates 6 TechMart company PDFs in `knowledge_base/`.

### 4. Build the vector store

```bash
python3 rag/ingest.py
```

Downloads the embedding model (~80MB on first run), chunks the PDFs, and builds the ChromaDB index in `rag/vectorstore/`.

### 5. Start the backend

```bash
uvicorn main:app --reload --port 8000
```

Test it: open `http://localhost:8000` — should return `{"status":"ok"}`.

### 6. Frontend setup

Open a second terminal:

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the frontend:

```bash
npm run dev
```

Open `http://localhost:3000` — you should see the login/signup screen.

---

## How it works

### Intent detection

Every message is sent to the LLM with a classification prompt. The model returns exactly one word (`billing`, `technical`, `product`, `complaint`, or `faq`), which determines which agent handles the query.

### RAG pipeline

Company PDFs are chunked into 500-character overlapping segments, embedded into vectors, and stored in ChromaDB. On each user message, the top 3 most semantically similar chunks are retrieved and injected into the agent's system prompt as context. The LLM answers using only this context — not its training data.

### Agent routing

```
User message
     ↓
detect_intent()  →  "billing"
     ↓
AGENT_MAP["billing"]  →  billing.answer()
     ↓
retrieve_context(message)  →  relevant PDF chunks
     ↓
LLM call with context  →  grounded reply
     ↓
save to MongoDB  →  return to frontend
```

### Authentication

Users sign up with email + password. Passwords are hashed with `bcrypt`. On login, a JWT token (expires in 7 days) is returned and stored in React state. Every API call includes `Authorization: Bearer <token>` in the header. Protected routes on the backend verify the token before responding.

---

## Deployment

### Backend → Render

1. Go to [render.com](https://render.com) → New Web Service → connect your GitHub repo
2. Set **Root Directory** to `backend`
3. Set **Build Command** to `pip install -r requirements.txt`
4. Set **Start Command** to `bash start.sh`
5. Add environment variables: `GROQ_API_KEY`, `MONGODB_URI`, `JWT_SECRET`
6. Deploy

**Note:** Render's free tier spins down after 15 minutes of inactivity. First request after a period of idle may take 30-60 seconds.

### Frontend → Vercel

1. Go to [vercel.com](https://vercel.com) → Add New Project → import your repo
2. Set **Root Directory** to `frontend`
3. Add environment variable: `NEXT_PUBLIC_API_URL` = your Render backend URL
4. Deploy

After deploying frontend, update `allow_origins` in `backend/main.py` with your Vercel URL and redeploy the backend.

---

## The five agents

| Agent | Handles | Key documents |
|---|---|---|
| Billing | Payments, refunds, invoices, EMI | RefundPolicy.pdf, Pricing.pdf |
| Technical | Login, bugs, installation, crashes | TechSupport.pdf |
| Product | Features, specs, comparisons, stock | Pricing.pdf, Products context |
| Complaint | Frustrated customers, escalations | All documents |
| FAQ | General info, hours, contact, shipping | FAQ.pdf, ShippingPolicy.pdf |

---

## Known limitations

- **Session not persisted across page refreshes** — token is stored in React state, not localStorage. Refreshing the page logs you out. This is by design for simplicity; a production system would use HTTP-only cookies.
- **Render cold starts** — free backend tier takes 30-60 seconds to wake from idle.
- **Knowledge base is static** — to update the company documents, re-run `rag/ingest.py` locally and push the updated `rag/vectorstore/` to GitHub.

---

## Local development cheatsheet

```bash
# Start backend
cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000

# Start frontend
cd frontend && npm run dev

# Rebuild vector store (after changing PDFs)
cd backend && source venv/bin/activate && python3 rag/ingest.py

# Test MongoDB connection
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); from pymongo import MongoClient; MongoClient(os.getenv('MONGODB_URI'), serverSelectionTimeoutMS=5000).server_info(); print('MongoDB OK')"

# Test Groq connection
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); from groq import Groq; r = Groq(api_key=os.getenv('GROQ_API_KEY')).chat.completions.create(model='openai/gpt-oss-20b',messages=[{'role':'user','content':'hi'}],max_tokens=10); print('Groq OK:', r.choices[0].message.content)"

# If port 8000 is stuck
lsof -i :8000 && kill -9 <PID>
```

---

## Built by

**Sandesh Avaradi**  
Built as a full-stack AI learning project over 4 weeks.
