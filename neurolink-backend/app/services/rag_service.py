from app.vector.chroma_client import collection


def store_memory_embedding(memory_id, text):

    collection.add(
        documents=[text],
        ids=[memory_id]
    )


def search_memories(query):

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    documents = results.get("documents")

    if documents and len(documents) > 0 and len(documents[0]) > 0:
        return " ".join(documents[0])

    return None