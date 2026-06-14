def chunk_text(text: str):
    """
    Chunk normalized dataset text using the '---' separator.
    Each chunk is a complete normalized entry with:
    [DATASET: name]
    [TYPE: category]
    Query: question
    Answer: response
    Details: metadata
    """
    chunks = []
    
    # Split by the '---' separator that delimits each normalized entry
    entries = text.split('---')
    
    for entry in entries:
        entry = entry.strip()
        
        # Skip empty entries
        if not entry:
            continue
        
        # Each normalized entry is already a complete, self-contained chunk
        # Minimum length check to filter out any malformed entries
        if len(entry) >= 50:  # Adjust this threshold as needed
            chunks.append(entry)
    
    return chunks


def chunk_text_with_overlap(text: str, max_chunk_size=1000, overlap=100):
    """
    Alternative chunking strategy for very long entries.
    Use this if some normalized entries are extremely long and you want to split them.
    
    Args:
        text: Input text to chunk
        max_chunk_size: Maximum characters per chunk
        overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    chunks = []
    
    # First split by '---' to get normalized entries
    entries = text.split('---')
    
    for entry in entries:
        entry = entry.strip()
        
        if not entry or len(entry) < 50:
            continue
        
        # If entry is short enough, keep it as one chunk
        if len(entry) <= max_chunk_size:
            chunks.append(entry)
        else:
            # For long entries, split them while preserving metadata
            lines = entry.split('\n')
            
            # Extract metadata (first few lines with [DATASET], [TYPE], Query, Answer)
            metadata_lines = []
            content_start_idx = 0
            
            for i, line in enumerate(lines):
                if line.startswith('[DATASET:') or line.startswith('[TYPE:') or \
                   line.startswith('Query:') or line.startswith('Answer:'):
                    metadata_lines.append(line)
                    content_start_idx = i + 1
                else:
                    break
            
            metadata = '\n'.join(metadata_lines)
            
            # If the entry is still too long, chunk the remaining content
            remaining_content = '\n'.join(lines[content_start_idx:])
            
            if len(remaining_content) <= max_chunk_size - len(metadata):
                chunks.append(entry)
            else:
                # Split long content into overlapping chunks
                words = remaining_content.split()
                current_chunk_words = []
                
                for word in words:
                    current_chunk_words.append(word)
                    current_text = ' '.join(current_chunk_words)
                    
                    if len(current_text) >= max_chunk_size - len(metadata) - overlap:
                        chunk = metadata + '\n' + current_text
                        chunks.append(chunk)
                        
                        # Keep last 'overlap' characters for next chunk
                        overlap_words = []
                        overlap_length = 0
                        for w in reversed(current_chunk_words):
                            overlap_length += len(w) + 1
                            overlap_words.insert(0, w)
                            if overlap_length >= overlap:
                                break
                        current_chunk_words = overlap_words
                
                # Add remaining words as final chunk
                if current_chunk_words:
                    chunk = metadata + '\n' + ' '.join(current_chunk_words)
                    chunks.append(chunk)
    
    return chunks


def chunk_text_adaptive(text: str, small_threshold=500, large_threshold=2000):
    """
    Adaptive chunking that handles different entry sizes intelligently.
    
    - Small entries (< small_threshold): Keep as single chunks
    - Medium entries (< large_threshold): Keep as single chunks
    - Large entries (>= large_threshold): Split with overlap
    
    This ensures small entries aren't lost and large entries are manageable.
    """
    chunks = []
    entries = text.split('---')
    
    for entry in entries:
        entry = entry.strip()
        
        if not entry or len(entry) < 50:
            continue
        
        if len(entry) < large_threshold:
            # Keep smaller entries intact
            chunks.append(entry)
        else:
            # Split very large entries
            sub_chunks = chunk_text_with_overlap(
                entry, 
                max_chunk_size=large_threshold,
                overlap=200
            )
            chunks.extend(sub_chunks)
    
    return chunks


# Default export - use the simple version for normalized data
def get_chunks(text: str, strategy='simple'):
    """
    Get chunks using specified strategy.
    
    Args:
        text: Input text to chunk
        strategy: 'simple' (default), 'overlap', or 'adaptive'
    
    Returns:
        List of text chunks
    """
    if strategy == 'overlap':
        return chunk_text_with_overlap(text)
    elif strategy == 'adaptive':
        return chunk_text_adaptive(text)
    else:
        return chunk_text(text)