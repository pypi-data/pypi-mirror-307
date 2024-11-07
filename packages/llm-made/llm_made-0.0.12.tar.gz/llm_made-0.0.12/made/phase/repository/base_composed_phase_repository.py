from abc import ABC, abstractmethod


class BaseComposedPhaseRepository(ABC):
    @abstractmethod
    def update_phase_states(self, env):
        pass

    @abstractmethod
    def update_env_states(self, env):
        pass

    @abstractmethod
    def break_cycle(self, phase_states):
        pass
