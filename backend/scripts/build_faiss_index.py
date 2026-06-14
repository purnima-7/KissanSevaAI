import os
import pickle
import faiss
import time
from tqdm import tqdm

os.environ["TOKENIZERS_PARALLELISM"] = "false"

from chunk_text import chunk_text
from create_embeddings import get_embeddings

# Update paths to use normalized data
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEXT_DIR = os.path.join(BASE_DIR, "data", "balanced_data")  
FAISS_DIR = os.path.join(BASE_DIR, "vector_store", "faiss_index")

os.makedirs(FAISS_DIR, exist_ok=True)

all_chunks = []
metadata = []

print("=" * 70)
print("🚀 BUILDING FAISS INDEX FROM NORMALIZED DATA")
print("=" * 70)
print(f"📂 Reading from: {TEXT_DIR}\n")

start_time = time.time()

# Process each normalized file
for file in sorted(os.listdir(TEXT_DIR)):
    if not file.endswith("_normalized.txt"):
        continue

    # Extract dataset name (remove '_normalized.txt')
    dataset_name = file.replace("_normalized.txt", "").lower()
    file_path = os.path.join(TEXT_DIR, file)

    print(f"📄 Processing: {file}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Chunk the normalized text
    chunks = chunk_text(text)

    print(f"   ✓ Created {len(chunks):,} chunks")

    # Store chunks with metadata
    for chunk in chunks:
        all_chunks.append(chunk)
        
        # Extract dataset and type from the chunk itself for better metadata
        dataset_tag = ""
        type_tag = ""
        
        lines = chunk.split('\n')
        for line in lines[:3]:  # Check first 3 lines
            if line.startswith('[DATASET:'):
                dataset_tag = line.replace('[DATASET:', '').replace(']', '').strip()
            elif line.startswith('[TYPE:'):
                type_tag = line.replace('[TYPE:', '').replace(']', '').strip()
        
        metadata.append({
            "source": dataset_name,
            "source_file": file,
            "dataset_tag": dataset_tag,
            "data_type": type_tag
        })

print("\n" + "=" * 70)
print(f"✅ Total chunks created: {len(all_chunks):,}")
print(f"⏱️  Chunking time: {time.time() - start_time:.2f}s")
print("=" * 70)

# --------------------------------------------------
# CREATE EMBEDDINGS
# --------------------------------------------------
print("\n🔧 Creating embeddings...")
embedding_start = time.time()

embeddings = get_embeddings(all_chunks)

print(f"⏱️  Embedding time: {time.time() - embedding_start:.2f}s")

# --------------------------------------------------
# BUILD FAISS INDEX
# --------------------------------------------------
print("\n🏗️  Building FAISS index...")

dimension = embeddings.shape[1]
print(f"   Dimension: {dimension}")
print(f"   Total vectors: {len(embeddings):,}")

# Choose index type based on dataset size
if len(embeddings) < 100000:
    # For smaller datasets, use flat index (exact search)
    index = faiss.IndexFlatL2(dimension)
    index_type = "IndexFlatL2 (Exact Search)"
else:
    # For larger datasets, use IVF for faster search
    nlist = min(int(len(embeddings) ** 0.5), 4096)  # Number of clusters
    quantizer = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
    
    print(f"   Training IVF index with {nlist} clusters...")
    index.train(embeddings)
    index_type = f"IndexIVFFlat (Fast Search, {nlist} clusters)"

# Add vectors to index
print(f"   Adding {len(embeddings):,} vectors to index...")
index.add(embeddings)

print(f"   ✓ Index type: {index_type}")

# --------------------------------------------------
# SAVE INDEX + METADATA
# --------------------------------------------------
print("\n💾 Saving FAISS index and metadata...")

index_path = os.path.join(FAISS_DIR, "knowledge.index")
metadata_path = os.path.join(FAISS_DIR, "metadata.pkl")
chunks_path = os.path.join(FAISS_DIR, "chunks.pkl")

faiss.write_index(index, index_path)

with open(metadata_path, "wb") as f:
    pickle.dump(metadata, f)

with open(chunks_path, "wb") as f:
    pickle.dump(all_chunks, f)

print(f"   ✓ Index saved: {index_path}")
print(f"   ✓ Metadata saved: {metadata_path}")
print(f"   ✓ Chunks saved: {chunks_path}")

# --------------------------------------------------
# STATISTICS
# --------------------------------------------------
print("\n" + "=" * 70)
print("📊 INDEX STATISTICS")
print("=" * 70)

# Count chunks per dataset
dataset_counts = {}
for meta in metadata:
    dataset = meta['dataset_tag'] if meta['dataset_tag'] else meta['source']
    dataset_counts[dataset] = dataset_counts.get(dataset, 0) + 1

print("\nChunks per dataset:")
for dataset, count in sorted(dataset_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"   {dataset:30} {count:>8,} chunks")

print("\n" + "=" * 70)
total_time = time.time() - start_time
print(f"✅ FAISS INDEX BUILT SUCCESSFULLY!")
print(f"⏱️  Total time: {total_time:.2f}s ({total_time/60:.2f} minutes)")
print(f"📦 Total chunks indexed: {len(all_chunks):,}")
print(f"🎯 Ready for RAG queries!")
print("=" * 70 + "\n")