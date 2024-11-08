from abc import ABC, abstractmethod


class RolePlayingRepository(ABC):
    @abstractmethod
    def init_chat(self, placeholders, phase_prompt):
        pass

    @abstractmethod
    def process_messages(self, messages):
        pass
