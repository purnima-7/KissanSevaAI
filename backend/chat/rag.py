from dotenv import load_dotenv
load_dotenv()

import os
print("GROQ_API_KEY loaded:", bool(os.environ.get("GROQ_API_KEY")))

import pickle
import faiss

os.environ["TOKENIZERS_PARALLELISM"] = "false"

from groq import Groq   # ✅ GROQ SDK

from backend.chat.prompts import SYSTEM_PROMPT
from backend.chat.embeddings import embed_text

from backend.chat.errors import (
    KnowledgeNotFoundError,
    TokenLimitExceededError,
    LLMServiceError
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

GROQ_MODEL_NAME = "llama-3.3-70b-versatile"   # Best for RAG

TOP_K = 6
MIN_CHUNK_LENGTH = 10
DEBUG = False   # Set True to debug


# --------------------------------------------------
# LOAD FAISS + DATA
# --------------------------------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FAISS_DIR = os.path.join(BASE_DIR, "vector_store", "faiss_index")

faiss_index = faiss.read_index(os.path.join(FAISS_DIR, "knowledge.index"))

with open(os.path.join(FAISS_DIR, "chunks.pkl"), "rb") as f:
    CHUNKS = pickle.load(f)

with open(os.path.join(FAISS_DIR, "metadata.pkl"), "rb") as f:
    METADATA = pickle.load(f)


# --------------------------------------------------
# FAISS RETRIEVAL
# --------------------------------------------------

def retrieve_relevant_chunks(question: str, top_k: int = TOP_K):
    question_embedding = embed_text(question)
    distances, indices = faiss_index.search(question_embedding, top_k)

    retrieved = []
    seen_texts = set()

    for idx in indices[0]:
        if 0 <= idx < len(CHUNKS):
            text = CHUNKS[idx].strip()

            if len(text) < MIN_CHUNK_LENGTH:
                continue
            if text in seen_texts:
                continue

            seen_texts.add(text)

            meta = METADATA[idx] if idx < len(METADATA) else {}

            retrieved.append({
                "text": text,
                "meta": meta
            })

    return retrieved


# --------------------------------------------------
# CONTEXT FORMATTER
# --------------------------------------------------

def format_context(retrieved_chunks):
    blocks = []

    for i, item in enumerate(retrieved_chunks, start=1):
        meta = item.get("meta", {})
        text = item.get("text", "")

        block = f"""
Document {i}
Source Dataset: {meta.get("source", "unknown")}
Source File: {meta.get("source_file", "unknown")}

{text}
""".strip()

        blocks.append(block)

    return "\n\n".join(blocks)


# --------------------------------------------------
# Groq ANSWER GENERATION
# --------------------------------------------------

def generate_answer(question, retrieved_chunks):
    if not retrieved_chunks:
        raise KnowledgeNotFoundError()

    context = format_context(retrieved_chunks)

    if DEBUG:
        print("\n===== CONTEXT SENT TO GROQ =====\n")
        print(context)
        print("\n================================\n")

    prompt = f"""
{SYSTEM_PROMPT}

Answer strictly using ONLY the context.
If the answer is not present, say exactly:
"I do not have information related to this question."

Context:
{context}

Question:
{question}
"""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        if response and response.choices:
            return response.choices[0].message.content.strip()

        raise LLMServiceError("Empty response from Groq")

    except Exception as e:
        error_msg = str(e).lower()
        print("Groq API Error:", e)

        if "rate limit" in error_msg or "token" in error_msg or "429" in error_msg:
            raise TokenLimitExceededError()

        raise LLMServiceError(str(e))



# --------------------------------------------------
# MAIN ENTRY
# --------------------------------------------------

def answer_question(question: str) -> str:
    retrieved_chunks = retrieve_relevant_chunks(question)

    if DEBUG:
        print("\n--- RAW RETRIEVED CHUNKS ---")
        for c in retrieved_chunks:
            print(c["text"])
        print("--- END RAW ---\n")

    return generate_answer(question, retrieved_chunks)
