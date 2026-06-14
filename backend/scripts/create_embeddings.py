import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


# MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # Fast and efficient
MODEL_NAME = "BAAI/bge-base-en-v1.5"  # Better model

# Load globally once — speeds up processing
print(f"🔧 Loading embedding model: {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)
print(f"✓ Model loaded successfully (dimension: {model.get_sentence_embedding_dimension()})")


def get_embeddings(text_chunks, batch_size=256, show_progress=True):
    """
    Generate embeddings for a list of text chunks using
    SentenceTransformer with batching for speed and memory safety.
    
    Args:
        text_chunks: List of text strings to embed
        batch_size: Number of chunks to process at once (adjust based on RAM)
        show_progress: Whether to show progress bar
    
    Returns:
        numpy array of embeddings with shape (num_chunks, embedding_dim)
    """
    
    all_embeddings = []
    
    print(f"\n🚀 Generating embeddings...")
    print(f"   Model: {MODEL_NAME}")
    print(f"   Total chunks: {len(text_chunks):,}")
    print(f"   Batch size: {batch_size}")
    print(f"   Estimated batches: {(len(text_chunks) + batch_size - 1) // batch_size}")
    
    # Create progress bar
    if show_progress:
        pbar = tqdm(total=len(text_chunks), desc="Embedding", unit="chunks")
    
    # Process in batches
    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i : i + batch_size]
        
        try:
            batch_embeddings = model.encode(
                batch,
                convert_to_numpy=True,
                normalize_embeddings=True,  # L2 normalization for FAISS
                show_progress_bar=False,
                batch_size=batch_size
            )
            
            all_embeddings.append(batch_embeddings)
            
            if show_progress:
                pbar.update(len(batch))
            
        except Exception as e:
            print(f"\n⚠️  Error processing batch {i//batch_size + 1}: {str(e)}")
            print(f"   Skipping {len(batch)} chunks...")
            continue
    
    if show_progress:
        pbar.close()
    
    # Combine all batches into one array
    if not all_embeddings:
        raise ValueError("No embeddings were created successfully!")
    
    embeddings = np.vstack(all_embeddings)
    
    print(f"\n✅ Embeddings created successfully!")
    print(f"   Shape: {embeddings.shape}")
    print(f"   Dimension: {embeddings.shape[1]}")
    print(f"   Total vectors: {embeddings.shape[0]:,}")
    print(f"   Memory size: {embeddings.nbytes / (1024**2):.2f} MB")
    
    return embeddings


def get_embedding_single(text):
    """
    Get embedding for a single text (useful for query encoding).
    
    Args:
        text: Single text string
    
    Returns:
        numpy array of shape (embedding_dim,)
    """
    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    return embedding


def get_model_info():
    """
    Get information about the loaded model.
    
    Returns:
        dict with model information
    """
    return {
        "model_name": MODEL_NAME,
        "embedding_dimension": model.get_sentence_embedding_dimension(),
        "max_seq_length": model.max_seq_length,
        "device": str(model.device)
    }


def test_embedding():
    """
    Test the embedding model with a sample text.
    """
    test_text = "What are the different methods of irrigation?"
    print(f"\n🧪 Testing embedding model...")
    print(f"   Test text: '{test_text}'")
    
    embedding = get_embedding_single(test_text)
    
    print(f"   ✓ Embedding shape: {embedding.shape}")
    print(f"   ✓ Embedding preview: {embedding[:5]}")
    print(f"   ✓ L2 norm: {np.linalg.norm(embedding):.6f} (should be ~1.0)")
    
    return embedding


if __name__ == "__main__":
    # Run test when script is executed directly
    print("=" * 70)
    print("EMBEDDING MODEL TEST")
    print("=" * 70)
    
    info = get_model_info()
    print("\n📋 Model Information:")
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    test_embedding()
    
    print("\n" + "=" * 70)
    print("✅ Embedding model is working correctly!")
    print("=" * 70)