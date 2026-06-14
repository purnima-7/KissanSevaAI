from sentence_transformers import SentenceTransformer

# Load once (IMPORTANT)
_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("BAAI/bge-base-en-v1.5")
    return _embedding_model


def embed_text(text: str):
    model = get_embedding_model()
    return model.encode([text])
