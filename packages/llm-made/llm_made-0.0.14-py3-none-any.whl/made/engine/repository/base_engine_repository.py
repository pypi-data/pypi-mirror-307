from abc import ABC, abstractmethod


class BaseEngineRepository(ABC):
    @abstractmethod
    def get_engine(self, model_config):
        pass
