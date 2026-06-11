from dotenv import load_dotenv
load_dotenv()
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
import numpy as np

# Nvidia provides free embedding models via NIM
embeddings = NVIDIAEmbeddings(model="nvidia/nv-embedqa-e5-v5")

texts = [
    "Beef production generates 60 kg CO2 per kg of meat",
    "Electric cars produce zero tailpipe emissions",
    "Solar panels reduce household carbon footprint by 80%",
    "The weather today is sunny and warm"
]

vectors = embeddings.embed_documents(texts)
print(f"Embedding dimension: {len(vectors[0])}")

query = "How much carbon does eating meat produce?"
query_vector = embeddings.embed_query(query)

def cosine_sim(a,b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

for text, vec in zip(texts, vectors):
    sim = cosine_sim(query_vector, vec)
    print(f"{sim:.4f} - {text}")
