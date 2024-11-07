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
class DefaultTestModificationPhaseRepositoryImpl(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config: ModelConfig,
        phase_prompt: str = PhasePrompt.test_modification,
        assistant_role_name: str = RoleType.PROGRAMMER,
        assistant_role_prompt: str = RolePrompt.PROGRAMMER,
        user_role_name: str = RoleType.TESTER,
        user_role_prompt: str = RolePrompt.TESTER,
        chat_turn_limit: int = PhaseChatTurnLimit.test_modification,
        **kwargs,
    ):
        phase_engine_config = PhaseEngineConfig.test_modification
        super().__init__(
            model_config=model_config,
            phase_prompt=phase_prompt,
            assistant_role_name=assistant_role_name,
            assistant_role_prompt=assistant_role_prompt,
            user_role_name=user_role_name,
            user_role_prompt=user_role_prompt,
            chat_turn_limit=chat_turn_limit,
            temperature=phase_engine_config.temperature,
            top_p=phase_engine_config.top_p,
            **kwargs,
        )

    def update_phase_states(self, env: ChatEnvRepositoryImpl):
        # TODO implement
        self.states.__dict__ = env.states.__dict__
        self.states.task = env.config.task_prompt
        self.states.description = env.states.task_description
        pass

    def update_env_states(self, env: ChatEnvRepositoryImpl) -> ChatEnvRepositoryImpl:
        env.states.test_reports = self.seminar_conclusion
        return env
