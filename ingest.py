import os

def load_documents(folder="documents"):
    docs = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append({"filename": filename, "text": text})
    return docs

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if len(chunk.strip()) > 0:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def ingest(folder="documents"):
    docs = load_documents(folder)
    all_chunks = []
    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": doc["filename"],
                "chunk_index": i
            })
    return all_chunks

if __name__ == "__main__":
    chunks = ingest()
    print(f"Total chunks: {len(chunks)}")
    for c in chunks[:5]:
        print(f"\n--- {c['source']} chunk {c['chunk_index']} ---")
        print(c['text'])
