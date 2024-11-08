from abc import ABC, abstractmethod


class BaseEngineService(ABC):
    @abstractmethod
    def chat_completion(self, messages, ollama_config):
        pass
    
    @abstractmethod
    def embedding(self, messages, ollama_config):
        pass
