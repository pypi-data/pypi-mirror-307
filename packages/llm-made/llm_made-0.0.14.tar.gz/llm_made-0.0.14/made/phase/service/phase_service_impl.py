from made.engine import ModelConfig
from made.phase import PhaseRegistry
from made.phase.service.phase_service import PhaseService


class PhaseServiceImpl(PhaseService):
    def __init__(
        self,
        model_config: ModelConfig,
    ):
        self.model_config = model_config

    def get_phase(
        self,
        phase_name: str,
        **kwargs,
    ):
        phase = PhaseRegistry.get(phase_name)(model_config=self.model_config, **kwargs)
        return phase
