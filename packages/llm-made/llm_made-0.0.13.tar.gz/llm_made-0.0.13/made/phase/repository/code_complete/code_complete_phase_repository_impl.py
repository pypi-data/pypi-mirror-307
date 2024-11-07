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
class DefaultCodeCompletePhaseRepositoryImpl(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config: ModelConfig,
        phase_prompt: str = PhasePrompt.code_complete,
        assistant_role_name: str = RoleType.PROGRAMMER,
        assistant_role_prompt: str = RolePrompt.PROGRAMMER,
        user_role_name: str = RoleType.CTO,
        user_role_prompt: str = RolePrompt.CTO,
        chat_turn_limit: int = PhaseChatTurnLimit.code_complete,
    ):
        phase_engine_config = PhaseEngineConfig.code_complete
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
        )

    def update_phase_states(self, env: ChatEnvRepositoryImpl):
        self.states.task = env.config.task_prompt
        self.states.modality = env.states.modality
        self.states.language = env.states.language
        self.states.codes = env.states.codes

    def update_env_states(self, env: ChatEnvRepositoryImpl) -> ChatEnvRepositoryImpl:
        available_extensions = ["py", "js", "cpp", "c", "h", "java"]
        all_files = [
            file
            for file in os.listdir(env.config.directory)
            if file.split(".")[-1] in available_extensions
        ]
        for file_name in all_files:
            self.states.unimplemented_file = (
                file_name
                + "\n"
                + "```"
                + file_name.split(".")[-1]
                + "\n"
                + self.states.codes[file_name]
                + "\n```"
            )
            implemented_file = self.chatting(
                env=env,
                task_prompt=env.config.task_prompt,
                phase_prompt=self.phase_prompt,
                assistant_role_name=self.assistant_role_name,
                assistant_role_prompt=self.assistant_role_prompt,
                user_role_name=self.user_role_name,
                user_role_prompt=self.user_role_prompt,
                placeholders=self.states,
                chat_turn_limit=self.chat_turn_limit,
            )

            content = FileToolRepositoryImpl.abstract_contents_from_text(
                implemented_file,
                regex=r"(.+?)\n```.*?\n(.*?)```",
            )
            self.states.codes[file_name] = content[file_name]

            FileToolRepositoryImpl.write_file(
                os.path.join(env.config.directory, file_name), content[file_name]
            )

            # TODO git tool should be used below.

        env.states.codes = self.states.codes
        return env

    def execute(self, env):
        self.update_phase_states(env)
        env = self.update_env_states(env)
        return env
