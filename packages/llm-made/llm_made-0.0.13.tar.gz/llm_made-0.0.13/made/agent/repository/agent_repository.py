from abc import ABC, abstractmethod


class AgentRepository(ABC):
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_info(self, id, usage, termination_reasons, num_tokens):
        pass

    @abstractmethod
    def init_messages(self):
        pass

    @abstractmethod
    def update_messages(self, message):
        pass
