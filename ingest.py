from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"  # Uses psycopg3!
collection_name = "portfolio"
vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
    embedding_length=1536,
)

docs = []

with open("rag_docs.txt", "r") as file:
    for line in file:
        docs.append(
            Document(
                page_content=line.strip(),
                metadata={
                    "id": len(docs) + 1,
                },
            )
        )

print(f"Number of docs to ingest: {len(docs)}")
for doc in docs:
    print(f"Doc ID: {doc.metadata['id']}, Content: {doc.page_content}")

key = input("\nAre you sure you want to ingest thoses docs in the DB ? y/_")
if (key=="y"):
    v = vector_store.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])
    print(v)
