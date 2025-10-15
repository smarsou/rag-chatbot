"""
A script to test the retrieval of documents from the Vector Database (PGVector).
"""
# Need to add the modules to the path for imports
import sys, os, logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from rag.embeddings import MyEmbedding
from rag.vectorstores import MyVectorStoreInterface
from dotenv import load_dotenv
load_dotenv()

embedding = MyEmbedding(api_base=os.getenv("EMBEDDING_API_BASE"))
vector_store_interface = MyVectorStoreInterface(embedding=embedding, connection=os.getenv("VECTOR_DB_CONNECTION"), collection_name=os.getenv("VECTOR_DB_COLLECTION"))
vector_store = vector_store_interface.get_vector_store()

print("Connection established successfully.")

while True:
    query = input("Enter your query : ")
    num_docs = input("How many documents do you want to retrieve ? (default 4) : ")
    if not num_docs:
        num_docs = "4"
    num_docs = int(num_docs)
    retrieved_docs = vector_store.similarity_search(query, k=num_docs)
    for i, doc in enumerate(retrieved_docs):
        print(str(i) + " : " + str(doc.page_content))
