from typing import List

from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from made.engine import ModelConfig
from made.phase.repository.base_composed_phase_repository import (
    BaseComposedPhaseRepository,
)
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.phase.service.phase_service_impl import PhaseServiceImpl
from made.phase.entity.phase_states import PhaseStates


class BaseComposedPhaseRepositoryImpl(BaseComposedPhaseRepository):
    def __init__(
        self, model_config: ModelConfig, phases: List[str], states, num_cycle: int = 1
    ):
        self.phase_service = PhaseServiceImpl(model_config)
        self.phases = [self.phase_service.get_phase(phase) for phase in phases]
        self.states = states if states else PhaseStates()
        self.num_cycle = num_cycle

    def update_phase_states(self, env: ChatEnvRepositoryImpl):
        raise NotImplementedError

    def update_env_states(self, env: ChatEnvRepositoryImpl):
        raise NotImplementedError

    def break_cycle(self, phase_states):
        raise NotImplementedError

    def execute(self, env: ChatEnvRepositoryImpl):
        self.update_phase_states(env)
        for _ in range(self.num_cycle):
            for phase in self.phases:
                if isinstance(phase, BasePhaseRepositoryImpl):
                    phase.states = self.states
                    phase.update_phase_states(env)
                    if self.break_cycle(phase.states):
                        return env

                    env = phase.execute(env)
                    if self.break_cycle(phase.states):
                        return env

                elif isinstance(phase, BaseComposedPhaseRepositoryImpl):
                    phase = self.phase_service.get_phase(phase.__class__.__name__)
                    env = phase.execute(env)

                else:
                    raise NotImplementedError
        env = self.update_env_states(env)
        return env
