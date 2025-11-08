PSX Trader Starter
==================
This is a starter full-stack project for a Pakistan Stock Exchange (PSX) trading app.
It contains:
- backend/: FastAPI backend (Python) with sample endpoints and simulated websocket feed
- frontend/: React + Vite starter app (JSX) that connects to the backend and displays sample charts

How to run (development):
1. Backend:
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
2. Frontend:
   cd frontend
   npm install
   npm run dev
3. Open browser to the frontend dev server (usually http://localhost:5173) and the backend at http://localhost:8000

Notes:
- This is a starter scaffold. You will need to add real PSX data feeds, broker API integration,
  authentication, database persistence and production hardening.
- The project includes a Dockerfile for the backend and a simple package.json for the frontend.
