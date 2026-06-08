import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("professor_reviews")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(question, k=4):
    query_embedding = model.encode([question]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    
    context = "\n\n".join([f"Source: {s}\n{c}" for s, c in zip(sources, chunks)])
    
    prompt = f"""You are a helpful assistant that answers questions about UIC professors based on student reviews.
Answer the question using ONLY the information provided in the documents below.
If the documents don't contain enough information to answer, say "I don't have enough information on that."
Always cite which professor and source file your answer comes from.

Documents:
{context}

Question: {question}
Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    answer = response.choices[0].message.content
    unique_sources = list(set(sources))
    
    return {"answer": answer, "sources": unique_sources}

if __name__ == "__main__":
    result = ask("Which professor is the best at UIC?")
    print("Answer:", result["answer"])
    print("Sources:", result["sources"])
