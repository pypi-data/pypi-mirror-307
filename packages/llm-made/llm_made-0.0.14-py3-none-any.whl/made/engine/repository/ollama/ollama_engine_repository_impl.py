from openai import OpenAI

from made.engine import ModelConfig
from made.engine.repository.base_engine_repository import BaseEngineRepository


class OllamaEngineRepositoryImpl(BaseEngineRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def get_engine(self, model_config: ModelConfig):
        engine = OpenAI(base_url=model_config.base_url, api_key=model_config.api_key)

        return engine
