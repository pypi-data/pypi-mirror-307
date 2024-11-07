import os

from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from made.engine import ModelConfig
from made.phase import PhaseRegistry
from made.phase.entity.phase_chat_turn_limit import PhaseChatTurnLimit
from made.phase.entity.phase_engine_config import PhaseEngineConfig
from made.phase.entity.phase_prompts import PhasePrompt
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.role_playing.entity.role_prompts import RolePrompt
from made.role_playing.entity.role_type import RoleType
from made.tools.file.repository.file_tool_repository_impl import FileToolRepositoryImpl


@PhaseRegistry.register()
class DefaultCodingPhaseRepositoryImpl(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config: ModelConfig,
        phase_prompt: str = PhasePrompt.coding,
        assistant_role_name: str = RoleType.PROGRAMMER,
        assistant_role_prompt: str = RolePrompt.PROGRAMMER,
        user_role_name: str = RoleType.CTO,
        user_role_prompt: str = RolePrompt.CTO,
        chat_turn_limit: int = PhaseChatTurnLimit.coding,
        **kwargs,
    ):
        phase_engine_config = PhaseEngineConfig.coding
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
        self.states.task = env.config.task_prompt
        self.states.modality = env.states.modality
        self.states.language = env.states.language

    def update_env_states(self, env: ChatEnvRepositoryImpl) -> ChatEnvRepositoryImpl:
        contents = FileToolRepositoryImpl.abstract_contents_from_text(self.seminar_conclusion)
        for k, v in contents.items():
            env.states.codes[k] = v
            FileToolRepositoryImpl.write_file(os.path.join(env.config.directory, k), v)
        return env
