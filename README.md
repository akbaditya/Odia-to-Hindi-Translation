# Odia to Hindi Translator

A Transformer-based neural machine translation model that translates Odia text into Hindi, with a Next.js frontend and a FastAPI backend.

**Live demo:** https://odia-to-hindi-translation.vercel.app

## What's inside

- Custom Transformer (encoder-decoder) built from scratch in PyTorch — no pretrained weights, no fine-tuning
- Beam search decoding for better translation quality
- Unicode-aware text preprocessing for Odia/Hindi scripts
- Next.js frontend deployed on Vercel
- FastAPI backend, Dockerized and deployed on Render

## Project structure

```
repository/
├── frontend/
│   ├── src/app/page.js
│   ├── src/components/
│   ├── src/lib/
│   │   └── api.js
│   ├── package.json
│   └── next.config.mjs
└── backend/
    ├── model/
    │   └── best_model.pt
    ├── vocab/
    │   ├── vocab_odia.pkl
    │   └── vocab_hindi.pkl
    ├── config.py
    ├── text_preprocessing.py
    ├── vocab.py
    ├── model.py
    ├── decoder.py
    ├── inference.py
    ├── main.py
    ├── requirements.txt
    └── Dockerfile
```

## How it works

**Backend**
1. `text_preprocessing.py` — cleans raw Odia text (removes noise, normalizes Unicode, strips unwanted characters)
2. `vocab.py` — loads the source (Odia) and target (Hindi) vocabularies
3. `model.py` — the Transformer architecture
4. `decoder.py` — beam search decoder that generates the Hindi translation
5. `inference.py` — loads the model and vocab once at startup, exposes a `translate()` function
6. `main.py` — FastAPI app that wraps `translate()` in a REST endpoint

**Frontend**
- `src/app/page.js` — main translation UI
- `src/lib/api.js` — calls the backend `/translate` endpoint, reading the backend URL from `NEXT_PUBLIC_API_URL`

## Running locally

**Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Test it:
```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "ଆପଣ କେମିତି ଅଛନ୍ତି"}'
```

**Frontend**
```bash
cd frontend
npm install
```

Create `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Then run:
```bash
npm run dev
```

## Running the backend with Docker

```bash
cd backend
docker build -t odia-hindi-api .
docker run -d -p 8000:8000 --name odia-hindi-api odia-hindi-api
```

## API

**POST** `/translate`

Request:
```json
{ "text": "ଆପଣ କେମିତି ଅଛନ୍ତି" }
```

Response:
```json
{
  "input_text": "ଆପଣ କେମିତି ଅଛନ୍ତି",
  "translated_text": "आप कैसे हैं"
}
```

**GET** `/health` — basic health check for uptime monitoring.

## Deployment

- **Backend**: Dockerized, deployed on Render's free tier (root directory `backend`), model weights and vocab files baked into the image, CPU-only PyTorch build to keep memory under free-tier limits.
- **Frontend**: Next.js app deployed on Vercel (root directory `frontend`), with `NEXT_PUBLIC_API_URL` set as an environment variable pointing to the Render backend URL.
- CORS on the backend is restricted to the Vercel deployment's origin.

> Note: the backend runs on Render's free tier, which spins down after periods of inactivity. The first request after idle time may take 30–50 seconds while the container cold-starts.

## Model details

- Custom Transformer with 4 encoder layers, 4 decoder layers, 8 attention heads, 256-dim embeddings
- Trained on an Odia-Hindi parallel corpus for 30 epochs
- Beam search decoding (beam size 5) for inference
- ~32M parameters, ~130MB checkpoint

## Notes

This is a personal/learning project exploring low-resource Indic language translation using a Transformer built entirely from scratch, rather than fine-tuning an existing pretrained model.
