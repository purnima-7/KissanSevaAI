# ---------------------------------------------
# CRITICAL: MUST BE AT TOP (before any ML import)
# ---------------------------------------------
import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ---------------------------------------------
# Standard imports (UNCHANGED)
# ---------------------------------------------
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import time

from backend.chat.multilingual_rag import answer_question_multilingual
from backend.chat.language import detect_language

from backend.chat.errors import (
    KnowledgeNotFoundError,
    TokenLimitExceededError,
    LLMServiceError
)


# =========================================================
# 🔹 ADDITION #1 — IMAGE IMPORTS (ONLY ADDITION)
# =========================================================
from fastapi import UploadFile, File, Form
import shutil
import uuid
from backend.image_models.inference import load_model, predict_image

# ---------------------------------------------
# FastAPI App (UNCHANGED)
# ---------------------------------------------
app = FastAPI(
    title="Farmer AI Chatbot API",
    description="Multilingual AI-powered assistant for farmers using RAG",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ---------------------------------------------
# CORS Configuration (UNCHANGED)
# ---------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------
# Request & Response Models (UNCHANGED)
# ---------------------------------------------
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    language: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    detected_language: str
    processing_time_ms: int
    success: bool = True

class HealthResponse(BaseModel):
    status: str
    version: str
    supported_languages: list[str]

class TranslateRequest(BaseModel):
    text: str
    target_language: str

# ---------------------------------------------
# Supported Languages (UNCHANGED)
# ---------------------------------------------
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "gu": "Gujarati",
    "mr": "Marathi",
    "pa": "Punjabi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "ur": "Urdu"
}

# =========================================================
# 🔹 ADDITION #2 — LOAD IMAGE MODELS (NO EXISTING CODE TOUCHED)
# =========================================================
DISEASE_MODEL, DISEASE_CLASSES = load_model(
    "disease",
    "backend/image_models/disease_classes.json"
)

INSECT_MODEL, INSECT_CLASSES = load_model(
    "insect",
    "backend/image_models/insect_classes.json"
)

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------------------------------------
# Existing Endpoints (UNCHANGED)
# ---------------------------------------------
@app.get("/")
async def root():
    return {
        "message": "Farmer AI Chatbot API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "chat_endpoint": "/chat"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "supported_languages": list(SUPPORTED_LANGUAGES.keys())
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    start_time = time.time()

    if request.language:
        detected_lang = request.language.lower()
    else:
        detected_lang = detect_language(request.question)

    try:
        answer = answer_question_multilingual(request.question)

        return ChatResponse(
            answer=answer,
            detected_language=detected_lang,
            processing_time_ms=int((time.time() - start_time) * 1000),
            success=True
        )

    except KnowledgeNotFoundError:
        return ChatResponse(
            answer="I don’t have this information.",
            detected_language=detected_lang,
            processing_time_ms=int((time.time() - start_time) * 1000),
            success=True
        )

    except TokenLimitExceededError:
        return ChatResponse(
            answer="Your token limit has been exceeded. Please try again later.",
            detected_language=detected_lang,
            processing_time_ms=int((time.time() - start_time) * 1000),
            success=False
        )

    except LLMServiceError:
        return ChatResponse(
            answer="The service is temporarily unavailable. Please try again later.",
            detected_language=detected_lang,
            processing_time_ms=int((time.time() - start_time) * 1000),
            success=False
        )


@app.post("/translate")
def translate_text_endpoint(req: TranslateRequest):
    from backend.chat.translate import translate_text
    translated = translate_text(req.text, req.target_language)
    return {"translated": translated}

# =========================================================
# 🔹 ADDITION #3 — IMAGE QUERY ENDPOINT (ONLY NEW ENDPOINT)
# =========================================================
@app.post("/image-query")
async def image_query(
    image: UploadFile = File(...),
    type: str = Form(...),
    language: Optional[str] = Form(None)
):
    start_time = time.time()

    if type not in ["disease", "insect"]:
        raise HTTPException(status_code=400, detail="type must be disease or insect")

    ext = image.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    image_path = os.path.join(UPLOAD_DIR, filename)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    if type == "disease":
        label, confidence = predict_image(image_path, DISEASE_MODEL, DISEASE_CLASSES)
        query = f"What is {label} disease and how to treat it?"
    else:
        label, confidence = predict_image(image_path, INSECT_MODEL, INSECT_CLASSES)
        query = f"What damage does {label} cause and how to control it?"

    detected_lang = language if language else "en"
    
    try:
        answer = answer_question_multilingual(query)
        
        # Translate the answer to the selected language if not English
        if detected_lang and detected_lang.lower() != "en":
            from backend.chat.translate import translate_text
            answer = translate_text(answer, detected_lang)
        
        success = True
    except KnowledgeNotFoundError:
        answer = "I don't have this information."
        
        # Translate error message too
        if detected_lang and detected_lang.lower() != "en":
            from backend.chat.translate import translate_text
            answer = translate_text(answer, detected_lang)
        
        success = True
    except TokenLimitExceededError:
        answer = "Your token limit has been exceeded. Please try again later."
        
        # Translate error message
        if detected_lang and detected_lang.lower() != "en":
            from backend.chat.translate import translate_text
            answer = translate_text(answer, detected_lang)
        
        success = False
    except LLMServiceError:
        answer = "The service is temporarily unavailable. Please try again later."
        
        # Translate error message
        if detected_lang and detected_lang.lower() != "en":
            from backend.chat.translate import translate_text
            answer = translate_text(answer, detected_lang)
        
        success = False


    return {
        "type": type,
        "prediction": label,
        "confidence": confidence,
        "answer": answer,
        "language": detected_lang,
        "processing_time_ms": int((time.time() - start_time) * 1000),
        "success": True
    }


# ---------------------------------------------
# Startup Event (UNCHANGED)
# ---------------------------------------------
@app.on_event("startup")
async def startup_event():
    print("🚜 Farmer AI Chatbot API running with Image + RAG support")
