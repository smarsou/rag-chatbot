from openai import OpenAI
import logging
import os
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

key = input("Enter your OpenAI API key : ")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=key)
connection = input("Paste the url for connection with the Postgres Vector database : ")
collection_name = "portfolio"
print(f"Trying connection using connection: {connection} and collection name: {collection_name}")
vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)
print("Connection established successfully.")

while True:
    query = input("Enter your query : ")
    num_docs = input("How many documents do you want to retrieve ? (default 4) : ")
    if not num_docs:
        num_docs = "4"
    num_docs = int(num_docs)
    retrieved_docs = vector_store.similarity_search(query, k=num_docs)
    print(retrieved_docs)
    for i, doc in enumerate(retrieved_docs):
        print(str(i) + " : " + str(doc.page_content))
