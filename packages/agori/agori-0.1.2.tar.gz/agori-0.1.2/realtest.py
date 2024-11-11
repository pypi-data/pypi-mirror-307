from agori.core.db import WorkingMemory
from cryptography.fernet import Fernet

# Generate a new encryption key (in practice, store this securely)
encryption_key = Fernet.generate_key()
print(f"Encryption key: {encryption_key}")
encryption_key = b'PppstkHs4KWxOPpJ8fyEzMdEVBiaKMpq1C5QgqPzkgU='
api_key="14a38573c7c04028af5e11f1e158ec71"
azure_endpoint="https://openaihumanvaluex.openai.azure.com/"
model_name="adaembedding"

# Initialize the secure database
db = WorkingMemory(
    api_key=api_key,
    api_endpoint=azure_endpoint,
    encryption_key=encryption_key,
    db_unique_id="my_secure_db3",
    model_name=model_name
)

# Create a new collection
collection_metadata = {
    "description": "Research papers database",
    "owner": "research_team"
}
collection = db.create_collection("research_papers", metadata=collection_metadata)

# Add documents with metadata
documents = [
    "Advances in Neural Networks",
    "Quantum Computing Overview",
    "Machine Learning Applications"
]
metadata_list = [
    {"author": "John Doe", "year": "2023"},
    {"author": "Jane Smith", "year": "2023"},
    {"author": "Bob Wilson", "year": "2024"}
]

# Add documents - they will be automatically encrypted
doc_ids = db.add_documents(
    collection_name="research_papers",
    documents=documents,
    metadatas=metadata_list
)

# Query the collection - results will be automatically decrypted
results = db.query_collection(
    collection_name="research_papers",
    query_texts=[" networks"],
    n_results=2
)

# Process results
for i, (doc, distance) in enumerate(zip(results["documents"][0], results["distances"][0])):
    print(f"Result {i+1}:")
    print(f"Document: {doc}")
    print(f"Similarity Score: {1 - distance}")  # Convert distance to similarity
    if "metadatas" in results:
        print(f"Metadata: {results['metadatas'][0][i]}")
    print()

db.drop_collection("research_papers")
db.cleanup_database()

