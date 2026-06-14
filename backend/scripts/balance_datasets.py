import os
import random

"""
Balance dataset sizes by sampling down large datasets.
This prevents large datasets (like FAQ with 55K entries) from drowning out smaller ones.
"""

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NORMALIZED_DIR = os.path.join(BASE_DIR, "data", "updated_cleaned_text")
BALANCED_DIR = os.path.join(BASE_DIR, "data", "balanced_data")

# Maximum entries per dataset (adjust as needed)
MAX_ENTRIES_PER_DATASET = 5000

os.makedirs(BALANCED_DIR, exist_ok=True)

def balance_dataset(input_file, output_file, max_entries):
    """
    Sample a dataset down to max_entries if it's larger.
    Keep all entries if it's smaller.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by separator
    entries = content.split('---')
    entries = [e.strip() for e in entries if e.strip()]
    
    original_count = len(entries)
    
    # Sample if too large
    if len(entries) > max_entries:
        print(f"   Sampling {len(entries):,} entries down to {max_entries:,}")
        entries = random.sample(entries, max_entries)
        sampled = True
    else:
        print(f"   Keeping all {len(entries):,} entries (under limit)")
        sampled = False
    
    # Write to output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n---\n'.join(entries))
    
    return original_count, len(entries), sampled


def main():
    print("=" * 70)
    print("📊 BALANCING DATASET SIZES")
    print("=" * 70)
    print(f"Max entries per dataset: {MAX_ENTRIES_PER_DATASET:,}\n")
    
    stats = []
    
    for file in sorted(os.listdir(NORMALIZED_DIR)):
        if not file.endswith("_normalized.txt"):
            continue
        
        input_path = os.path.join(NORMALIZED_DIR, file)
        output_path = os.path.join(BALANCED_DIR, file)
        
        print(f"📄 Processing: {file}")
        
        original, final, sampled = balance_dataset(input_path, output_path, MAX_ENTRIES_PER_DATASET)
        
        stats.append({
            'file': file,
            'original': original,
            'final': final,
            'sampled': sampled,
            'reduction': ((original - final) / original * 100) if sampled else 0
        })
        
        print()
    
    # Summary
    print("=" * 70)
    print("📊 BALANCING SUMMARY")
    print("=" * 70)
    
    total_original = sum(s['original'] for s in stats)
    total_final = sum(s['final'] for s in stats)
    
    print(f"\n{'Dataset':<30} {'Original':>12} {'Final':>12} {'Change':>10}")
    print("-" * 70)
    
    for s in stats:
        change = f"-{s['reduction']:.1f}%" if s['sampled'] else "No change"
        print(f"{s['file'][:28]:<30} {s['original']:>12,} {s['final']:>12,} {change:>10}")
    
    print("-" * 70)
    print(f"{'TOTAL':<30} {total_original:>12,} {total_final:>12,} {'-' + str(round((total_original-total_final)/total_original*100, 1)) + '%':>10}")
    
    print("\n✅ Balanced datasets saved to:", BALANCED_DIR)
    print("\n💡 NEXT STEPS:")
    print("   1. Update build_faiss_index.py to use balanced_data instead of normalized_data")
    print("   2. Rebuild the FAISS index: python build_faiss_index.py")
    print("   3. Test again: python test_rag_system.py")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    main()