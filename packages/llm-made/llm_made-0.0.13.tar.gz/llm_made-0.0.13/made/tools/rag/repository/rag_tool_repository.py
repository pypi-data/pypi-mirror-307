from abc import ABC, abstractmethod


class RAGToolRepository(ABC):
    @staticmethod
    @abstractmethod
    def get_client(client_path):
        pass

    @staticmethod
    @abstractmethod
    def get_collection(client, collection_name):
        pass

    @staticmethod
    @abstractmethod
    def ingest(collection, documents):
        pass

    @staticmethod
    @abstractmethod
    def search(query):
        pass
