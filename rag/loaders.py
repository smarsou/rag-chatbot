from abc import ABC, abstractmethod
from typing_extensions import override
from langchain_community.document_loaders import PyPDFLoader
from typing import List
from langchain_core.documents import Document

class LoaderInterface(ABC):
    """
    An interface for document loaders.

    Should implement a `load` method that takes file paths as input
    and returns a list of Document objects.
    """
    @abstractmethod
    def load(self, *filepaths: str) -> List[Document]:
        pass


class PDFLoader(LoaderInterface):
    """A class to load PDF documents from specified filepaths."""

    @override
    def load(self, *filepaths: str) -> List[Document]:
        """
        Load one or more PDF files as LangChain Documents.
        """
        documents = []
        for path in filepaths:
            loader = PyPDFLoader(path)
            documents.extend(loader.load())
        return documents
