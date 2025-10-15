import os
from typing_extensions import override
from langchain_core.embeddings.embeddings import Embeddings
from langchain_postgres import PGVector
from abc import ABC, abstractmethod

class VectorStoreInterface(ABC):
    """
    An interface for vector stores.
    Should implement methods to get the vector store instance
    and to add documents to the store. 
    """
    @abstractmethod
    def get_vector_store(self):
        pass

    @abstractmethod
    def add_documents(self, documents, ids=None):
        pass

class MyVectorStoreInterface(VectorStoreInterface):
    """
    A class to manage the vector store using PGVector and custom embeddings.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Implementing Singleton pattern to ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super(MyVectorStoreInterface, cls).__new__(cls)
        return cls._instance

    def __init__(self, embedding: Embeddings, connection: str, collection_name: str):
        self._connection = connection
        self._collection_name = collection_name
        self.vector_store = PGVector(
            embeddings=embedding,
            collection_name=self._collection_name,
            connection=self._connection,
            use_jsonb=True,
            embedding_length=384
        )

    @override
    def get_vector_store(self):
        return self.vector_store
    
    @override
    def add_documents(self, documents, ids=None):
        return self.vector_store.add_documents(documents, ids=ids)