# FastAPI Groq Chat

Simple FastAPI app with a `/chat` endpoint that forwards conversation history to Groq's `llama-3.3-70b-versatile` model.

Usage

1. Copy `.env.example` to `.env` and set `GROQ_API_KEY`.
2. Install deps:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python main.py
```

POST /chat
- Input JSON: `{ "message": "Hello", "conversation_id": "optional-id" }`
- Response JSON: `{ "response": "<assistant reply>", "conversation_id": "..." }`

Notes
- CORS is enabled for all origins.
- Conversation history is kept in-memory for the process lifetime.
- Adjust the Groq API endpoint in `main.py` if your account uses a different URL/payload.
