import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(
    path="./chroma",
    settings=Settings(anonymized_telemetry=False)
)

collection = client.get_or_create_collection(name="sales_knowledge")

documents = [
    "Leads with high website engagement and recent activity should be prioritized as HOT.",
    "Working professionals and business owners have higher conversion likelihood.",
    "Leads with no activity in the last 30 days should be downgraded unless strong intent exists.",
    "Do Not Call or Do Not Email flags reduce lead priority significantly.",
    "HOT leads should be contacted within 24 hours for best conversion.",
    "WARM leads require nurturing through follow-ups.",
    "COLD leads should be deprioritized or re-engaged later."
]

collection.add(
    documents=documents,
    ids=[f"doc_{i}" for i in range(len(documents))]
)

print("Vector DB ingested successfully.")