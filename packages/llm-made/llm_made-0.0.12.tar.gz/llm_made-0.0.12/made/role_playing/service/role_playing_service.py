from abc import ABC, abstractmethod


class RolePlayingService(ABC):
    @abstractmethod
    def step(self, user_message, assistant_only):
        pass
