import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(
    path="./chroma",
    settings=Settings(anonymized_telemetry=False)
)

collection = client.get_collection(name="sales_knowledge")

def retrieve_context(query: str, k: int = 3):
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    # Returns the list of matching documents
    return results["documents"][0]
