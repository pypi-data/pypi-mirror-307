from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from made.engine import ModelConfig
from made.phase import PhaseRegistry
from made.phase.entity.phase_chat_turn_limit import PhaseChatTurnLimit
from made.phase.entity.phase_engine_config import PhaseEngineConfig
from made.phase.entity.phase_prompts import PhasePrompt
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.role_playing.entity.role_prompts import RolePrompt
from made.role_playing.entity.role_type import RoleType


@PhaseRegistry.register()
class DefaultDemandAnalysisPhaseRepositoryImpl(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config: ModelConfig,
        phase_prompt: str = PhasePrompt.demand_analysis,
        assistant_role_name: str = RoleType.CPO,
        assistant_role_prompt: str = RolePrompt.CPO,
        user_role_name: str = RoleType.CEO,
        user_role_prompt: str = RolePrompt.CEO,
        chat_turn_limit: int = PhaseChatTurnLimit.demand_analysis,
        conversation_rag: bool = True,
        **kwargs,
    ):
        phaes_engine_config = PhaseEngineConfig.demand_analysis
        super().__init__(
            model_config=model_config,
            phase_prompt=phase_prompt,
            assistant_role_name=assistant_role_name,
            assistant_role_prompt=assistant_role_prompt,
            user_role_name=user_role_name,
            user_role_prompt=user_role_prompt,
            chat_turn_limit=chat_turn_limit,
            conversation_rag=conversation_rag,
            temperature=phaes_engine_config.temperature,
            top_p=phaes_engine_config.top_p,
            **kwargs,
        )

    def update_phase_states(self, env: ChatEnvRepositoryImpl):
        pass

    def update_env_states(self, env: ChatEnvRepositoryImpl) -> ChatEnvRepositoryImpl:
        env.states.modality = self.seminar_conclusion
        return env
