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
class DefaultLanguageChoosePhaseRepositoryImpl(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config: ModelConfig,
        phase_prompt: str = PhasePrompt.language_choose,
        assistant_role_name: str = RoleType.CTO,
        assistant_role_prompt: str = RolePrompt.CTO,
        user_role_name: str = RoleType.CEO,
        user_role_prompt: str = RolePrompt.CEO,
        chat_turn_limit: int = PhaseChatTurnLimit.language_choose,
        conversation_rag: bool = True,
        **kwargs
    ):
        phase_engine_config = PhaseEngineConfig.language_choose
        super().__init__(
            model_config=model_config,
            phase_prompt=phase_prompt,
            assistant_role_name=assistant_role_name,
            assistant_role_prompt=assistant_role_prompt,
            user_role_name=user_role_name,
            user_role_prompt=user_role_prompt,
            chat_turn_limit=chat_turn_limit,
            conversation_rag=conversation_rag,
            temperature=phase_engine_config.temperature,
            top_p=phase_engine_config.top_p,
            **kwargs
        )

    def update_phase_states(self, env: ChatEnvRepositoryImpl):
        # TODO implement
        self.states.task = env.config.task_prompt
        self.states.modality = env.states.modality

    def update_env_states(self, env: ChatEnvRepositoryImpl) -> ChatEnvRepositoryImpl:
        env.states.language = self.seminar_conclusion
        return env
