Planner Server (Groq-backed NL to Actions)

Overview:
- A minimal FastAPI server that exposes POST /plan to translate a natural language command into a sequence of UI actions using Groq.
- Secrets are read from environment variables. See planner_server/.env.example.

Usage:
- Install dependencies: pip install -r requirements.txt
- Run: uvicorn main:app --reload --port 8000
- Example:
  curl -X POST http://localhost:8000/plan -H 'Content-Type: application/json' -d '{"nl": "Open Settings and enable Wi-Fi"}'

Note:
- The Groq API keys must be provided via environment variables GROQ_CHAT_API_KEY, GROQ_CODING_API_KEY, GROQ_COMPOUND_API_KEY.
- The client currently only uses the chat-based NL → actions path. Extend as needed for more capabilities.
