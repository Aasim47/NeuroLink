import chromadb
from chromadb.config import Settings

# Persistent client
client = chromadb.PersistentClient(path="chroma_db")

# Create / load collection
collection = client.get_or_create_collection(
    name="memory_embeddings"
)