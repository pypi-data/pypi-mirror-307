from abc import ABC, abstractmethod


class Agentservice(ABC):
    @abstractmethod
    def step(self, user_message, assistant_only):
        pass
