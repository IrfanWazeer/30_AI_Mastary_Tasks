# FastAPI Groq Chat Example

Requirements:
- Python 3.10+
- A Groq API key set as `GROQ_API_KEY` in a `.env` file

Install:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file next to `Using_FastAPI.py`:

```
GROQ_API_KEY=your_real_groq_api_key_here

# Optional: enable mock mode for offline testing (no external API calls)
# MOCK_MODE=true
```

Run the app:

```bash
uvicorn Using_FastAPI:app --reload --host 0.0.0.0 --port 8000
```

Endpoint:

- `POST /chat` - JSON body: `{ "message": "Hello" }`. Returns `{ "reply": "...", "history": [...] }`.

Mock mode:

 - Set `MOCK_MODE=true` in your `.env` to enable a deterministic offline reply for testing.
