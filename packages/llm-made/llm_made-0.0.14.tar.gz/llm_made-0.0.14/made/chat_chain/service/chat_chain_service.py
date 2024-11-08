from abc import ABC, abstractmethod


class ChatChainService(ABC):
    @abstractmethod
    def get_phases(self):
        pass

    @abstractmethod
    def run(self):
        pass
