from typing import List

import chromadb
from chromadb.api import ClientAPI
from chromadb import Collection

from made.tools.rag.repository.rag_tool_repository import RAGToolRepository
from made.engine import ModelConfig
from made.engine.service.ollama.ollama_engine_service_impl import (
    OllamaEngineServiceImpl,
)


class RAGToolRepositoryImpl(RAGToolRepository):
    @staticmethod
    def get_client(persist_path: str) -> ClientAPI:
        client = chromadb.PersistentClient(path=persist_path)
        return client

    @staticmethod
    def get_collection(client: ClientAPI, collection_name: str) -> Collection:
        collection = client.get_or_create_collection(name=collection_name)
        return collection

    @staticmethod
    def ingest(
        collection: Collection, documents: List[str], model_config: ModelConfig
    ) -> None:
        engine = OllamaEngineServiceImpl.get_instance()
        for idx, document in enumerate(documents):
            embeddings = engine.embedding(document, model_config).data[0].embedding
            collection.add(
                ids=[str(idx)], embeddings=[embeddings], documents=[document]
            )

    @staticmethod
    def search(
        query: str,
        collection: Collection,
        model_config: ModelConfig,
        n_results: int = 3,
    ) -> List[str]:
        engine = OllamaEngineServiceImpl.get_instance()
        query_embeddings = engine.embedding(query, model_config).data[0].embedding
        search_results = collection.query(
            query_embeddings=query_embeddings, n_results=n_results
        )["documents"][0][:n_results]
        return search_results
