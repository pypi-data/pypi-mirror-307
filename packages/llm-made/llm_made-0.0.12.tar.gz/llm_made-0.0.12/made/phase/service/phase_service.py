from abc import ABC, abstractmethod


class PhaseService(ABC):
    @abstractmethod
    def get_phase(self, phase_name):
        pass
