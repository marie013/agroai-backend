import os
import faiss
import numpy as np
from openai import OpenAI
from pathlib import Path
import pickle

INDEX_PATH = Path("data/faiss.index")
META_PATH = Path("data/faiss_meta.pkl")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def semantic_search(query: str, k: int = 3):
    if not INDEX_PATH.exists() or not META_PATH.exists():
        return []
    
    index = faiss.read_index(str(INDEX_PATH))
    with META_PATH.open("rb") as f:
        metadata = pickle.load(f)

    q_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
        ).data[0].embedding
    q_vec = np.array([q_embedding]).astype("float32")

    distances, indexes = index.search(q_vec, k)
    results = []
    for idx in indexes[0]:
        if idx < len(metadata):
            results.append(metadata[idx])
    return results
def rag_answer(query:str) ->str:
    docs = semantic_search(query)
    context = "\n".join([chunk for _, chunk in docs])
    prompt = f"""
Responde la siguiente pregunta basándote en los documentos agrícolas cargados.
Si no encuentras respuesta, di que no tienes información suficiente.
Pregunta: {query}
Contexto = \n{context}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system", "content":"eres un asistente expero en agronomía"}, {"role":"user", "content": prompt}]
    )
    return response.choices[0].message.content