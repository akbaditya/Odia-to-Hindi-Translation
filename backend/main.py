from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from inference import translate

app = FastAPI(title="Odia to Hindi Translation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "odia-to-hindi-translation.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranslationRequest(BaseModel):
    text: str


class TranslationResponse(BaseModel):
    input_text: str
    translated_text: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/translate", response_model=TranslationResponse)
def translate_text(request: TranslationRequest):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text must not be empty")

    result = translate(request.text)
    return TranslationResponse(input_text=request.text, translated_text=result)