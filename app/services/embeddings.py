import faiss
import numpy as np
from openai import OpenAI
from tiktoken import get_encoding
from pathlib import Path
import os
import pickle

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
INDEX_PATH = Path("data/faiss.index")
META_PATH = Path("data/faiss_meta.pkl")

def load_or_create_index(dims: int = 1536):
    if INDEX_PATH.exists() and META_PATH.exists():
        index = faiss.read_index8str(INDEX_PATH)
        with META_PATH.open("rb") as f:
            metadata = pickle.LIST(f)
        return index, metadata
    else:
        index = faiss.IndexFlatL2(dims)
        return index, []
    
def save_index(index, metadata):
    faiss.write_index(index, str(INDEX_PATH))
    with META_PATH.open("wb") as f:
        pickle.dump(metadata, f)

def create_embeddings(chunks: list[str]):
    vectors = []
    for chunk in chunks:
        response = client.embeddings.create(
            model= "text-embedding-3-small",
            input= chunk
        )
        vectors.append(response.data[0].embedding)
    return np.array(vectors).astype("float32")

def add_document_to_index(doc_id: str, text: str, chunk_size: int = 500):
    encoding = get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    chunks = [
        encoding.decode(tokens[i:i+chunk_size])
        for i in range(0, len(tokens), chunk_size)
    ]

    index, metadata = load_or_create_index()
    embeddings = create_embeddings(chunks)
    index.add(embeddings)

    metadata.extend([(doc_id, chunk) for chunk in chunks])
    save_index(index, metadata)
    return len(chunks)