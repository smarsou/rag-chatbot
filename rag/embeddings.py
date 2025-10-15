from typing_extensions import override
import requests
from langchain_core.embeddings.embeddings import Embeddings

class MyEmbeddingModelAPI:
    """
    A class to interact with a custom embedding model accessible from a custom REST API.
    """

    def __init__(self, api_base: str):
        self.api_base = api_base

    def request_embedding(self, input: str):
        """
        Request an embedding for a string from the custom API.

        The custom API should follow the OpenAI embedding API format.
        """
        response = requests.post(
            f"{self.api_base}/v1/embeddings",
            headers={"Content-Type": "application/json"},
            json={"input": input}
        )

        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")

        return response.json()['data'][0]['embedding']

class MyEmbedding(Embeddings):
    """
    Custom Embedding class which implements the LangChain Embeddings interface.
    
    It uses the EmbeddingModelAPI class to get embeddings.
    """

    def __init__(self, api_base : str):
        super().__init__()
        self.api = MyEmbeddingModelAPI(api_base=api_base)
    
    @override
    def embed_documents(self, texts : list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            embedding = self.api.request_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    @override
    def embed_query(self, text : str) -> list[float]:
        return self.api.request_embedding(text)

