import os
import pickle
import faiss
import numpy as np
from create_embeddings import get_embedding_single

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FAISS_DIR = os.path.join(BASE_DIR, "vector_store", "faiss_index")

def load_rag_system():
    """Load the FAISS index and associated data"""
    print("📂 Loading RAG system...")
    
    index_path = os.path.join(FAISS_DIR, "knowledge.index")
    metadata_path = os.path.join(FAISS_DIR, "metadata.pkl")
    chunks_path = os.path.join(FAISS_DIR, "chunks.pkl")
    
    # Load FAISS index
    index = faiss.read_index(index_path)
    
    # Load metadata
    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)
    
    # Load chunks
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)
    
    print(f"✓ Loaded {index.ntotal:,} vectors")
    print(f"✓ Loaded {len(chunks):,} chunks")
    print(f"✓ Loaded {len(metadata):,} metadata entries\n")
    
    return index, chunks, metadata


def search(query, index, chunks, metadata, k=5):
    """
    Search the RAG system for relevant chunks.
    
    Args:
        query: User's question
        index: FAISS index
        chunks: List of text chunks
        metadata: List of metadata dicts
        k: Number of results to return
    
    Returns:
        List of (chunk, distance, metadata) tuples
    """
    # Get query embedding
    query_embedding = get_embedding_single(query)
    query_embedding = query_embedding.reshape(1, -1)
    
    # Search FAISS index
    distances, indices = index.search(query_embedding, k)
    
    # Collect results
    results = []
    for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        if idx < len(chunks):  # Valid index
            results.append({
                'rank': i + 1,
                'chunk': chunks[idx],
                'distance': float(dist),
                'similarity': 1 / (1 + float(dist)),  # Convert distance to similarity
                'metadata': metadata[idx]
            })
    
    return results


def format_result(result):
    """Format a single search result for display"""
    lines = result['chunk'].split('\n')
    
    # Extract key information
    dataset = ""
    data_type = ""
    query = ""
    answer = ""
    
    for line in lines:
        if line.startswith('[DATASET:'):
            dataset = line.replace('[DATASET:', '').replace(']', '').strip()
        elif line.startswith('[TYPE:'):
            data_type = line.replace('[TYPE:', '').replace(']', '').strip()
        elif line.startswith('Query:'):
            query = line.replace('Query:', '').strip()
        elif line.startswith('Answer:'):
            answer = line.replace('Answer:', '').strip()
    
    print(f"\n{'─' * 70}")
    print(f"🎯 Rank #{result['rank']}")
    print(f"📊 Dataset: {dataset}")
    print(f"🏷️  Type: {data_type}")
    print(f"📏 Similarity: {result['similarity']:.4f}")
    print(f"{'─' * 70}")
    
    if query:
        print(f"\n❓ Query: {query}")
    if answer:
        print(f"\n💡 Answer: {answer}")
    
    # Show full chunk if requested
    # print(f"\n📄 Full Chunk:\n{result['chunk']}")


def test_queries():
    """Run test queries from different datasets"""
    
    test_cases = [
        {
            "query": "What are the different methods of irrigation?",
            "expected_dataset": "call_query",
            "description": "General Knowledge Query"
        },
        {
            "query": "When to plant paddy in Rajasthan?",
            "expected_dataset": "crop_calendar",
            "description": "Crop Calendar Query"
        },
        {
            "query": "What was the gram production in Banswara in 2008?",
            "expected_dataset": "crop_production",
            "description": "Production Statistics Query"
        },
        {
            "query": "How to control aphid infestation in mustard crops?",
            "expected_dataset": ["faq", "pesticide_remedy"],  # Accept both!
            "description": "Expert Advice Query"
        },
        {
            "query": "What fertilizer should I use for wheat in loamy soil?",
            "expected_dataset": ["fertilizer_recommendation", "faq", "call_query"],  # Accept multiple
            "description": "Fertilizer Recommendation Query"
        },
        {
            "query": "How to treat leaf spot disease in turmeric?",
            "expected_dataset": ["pesticide_remedy", "faq"],  # Accept both
            "description": "Disease Treatment Query"
        },
        {
            "query": "What pesticides are effective against alfalfa weevil?",
            "expected_dataset": "pest_control",
            "description": "Pest Control Query"
        }
    ]
    
    print("\n" + "=" * 70)
    print("🧪 TESTING RAG SYSTEM WITH SAMPLE QUERIES")
    print("=" * 70)
    
    # Load RAG system
    index, chunks, metadata = load_rag_system()
    
    # Run tests
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n\n{'═' * 70}")
        print(f"TEST {i}/{len(test_cases)}: {test['description']}")
        print(f"{'═' * 70}")
        print(f"\n🔍 Query: \"{test['query']}\"")
        print(f"📁 Expected Dataset: {test['expected_dataset']}")
        
        # Search - increased k to see more results
        results = search(test['query'], index, chunks, metadata, k=10)
        
        # Check if top result is from expected dataset
        if results:
            top_result = results[0]
            top_dataset = top_result['metadata'].get('dataset_tag', 
                                                     top_result['metadata'].get('source', ''))
            
            # Display top 3 results
            for result in results:
                format_result(result)
            
            # Verify - handle both string and list expected datasets
            expected = test['expected_dataset']
            
            if isinstance(expected, list):
                # If expected is a list, check if any match
                if any(exp in top_dataset.lower() for exp in expected):
                    print(f"\n✅ TEST PASSED: Correct dataset retrieved!")
                    passed += 1
                else:
                    print(f"\n❌ TEST FAILED: Expected one of {expected}, got '{top_dataset}'")
                    failed += 1
            else:
                # If expected is a string, check normally
                if expected in top_dataset.lower():
                    print(f"\n✅ TEST PASSED: Correct dataset retrieved!")
                    passed += 1
                else:
                    print(f"\n❌ TEST FAILED: Expected '{expected}', got '{top_dataset}'")
                    failed += 1
        else:
            print(f"\n❌ TEST FAILED: No results found!")
            failed += 1
    
    # Summary
    print(f"\n\n{'═' * 70}")
    print("📊 TEST SUMMARY")
    print(f"{'═' * 70}")
    print(f"✅ Passed: {passed}/{len(test_cases)}")
    print(f"❌ Failed: {failed}/{len(test_cases)}")
    print(f"📈 Success Rate: {(passed/len(test_cases)*100):.1f}%")
    print("=" * 70 + "\n")


def interactive_search():
    """Interactive search mode"""
    print("\n" + "=" * 70)
    print("🔍 INTERACTIVE SEARCH MODE")
    print("=" * 70)
    print("Type your questions, or 'quit' to exit\n")
    
    # Load RAG system
    index, chunks, metadata = load_rag_system()
    
    while True:
        query = input("\n❓ Your question: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not query:
            continue
        
        print(f"\n🔍 Searching for: \"{query}\"")
        results = search(query, index, chunks, metadata, k=3)
        
        if results:
            print(f"\n📊 Found {len(results)} relevant results:")
            for result in results:
                format_result(result)
        else:
            print("\n⚠️ No results found!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_search()
    else:
        test_queries()