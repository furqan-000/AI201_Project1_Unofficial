import chromadb
from sentence_transformers import SentenceTransformer
from ingest import ingest

def embed_and_store():
    chunks = ingest()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    try:
        client.delete_collection("professor_reviews")
    except:
        pass
    
    collection = client.create_collection("professor_reviews")
    
    texts = [c["text"] for c in chunks]
    sources = [c["source"] for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    
    print("Embedding chunks...")
    embeddings = model.encode(texts).tolist()
    
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"source": s} for s in sources],
        ids=ids
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB")

if __name__ == "__main__":
    embed_and_store()
