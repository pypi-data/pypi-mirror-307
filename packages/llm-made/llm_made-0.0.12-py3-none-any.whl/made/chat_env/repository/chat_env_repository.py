from abc import ABC, abstractmethod


class ChatEnvRepository(ABC):
    @abstractmethod
    def reset(self, env_config, env_states):
        pass
