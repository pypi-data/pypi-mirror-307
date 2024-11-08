import os
import pickle
from typing import List, Tuple, Optional

from made.chat_chain.repository.chat_chain_repository import ChatChainRepository
from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.tools.file.repository.file_tool_repository_impl import FileToolRepositoryImpl
from made.tools.git.repository.git_tool_repository_impl import GitToolRepositoryImpl


class ChatChainRepositoryImpl(ChatChainRepository):
    def execute_step(
        self,
        env: ChatEnvRepositoryImpl,
        phase: BasePhaseRepositoryImpl,
    ):
        phase.execute(env)

    def execute_chain(
        self,
        env: ChatEnvRepositoryImpl,
        phases: List[BasePhaseRepositoryImpl],
        save_chain: bool = False,
        file_path: Optional[str] = None,
        phase_idx: Optional[int] = -1
    ):
        for phase in phases:
            if save_chain:
                ChatChainRepositoryImpl.save_chain(
                    file_path=file_path,
                    global_env=env,
                    phase_name=phase.__class__.__name__,
                    phase_idx=phase_idx,
                )
            self.execute_step(env=env, phase=phase)
            if save_chain:
                ChatChainRepositoryImpl.save_chain(
                    file_path=file_path,
                    global_env=env,
                    phase_name=phase.__class__.__name__,
                    phase_idx=phase_idx,
                )
            phase_idx += 1
        if save_chain:
            ChatChainRepositoryImpl.save_chain(
                file_path=file_path,
                global_env=env,
                phase_name="Done",
                phase_idx=phase_idx,
            )

    def preprocessing(self, env: ChatEnvRepositoryImpl):
        workspace = os.path.join(env.config.directory)
        os.makedirs(workspace, exist_ok=True)
        log_path = os.path.join(workspace, "logs")
        os.makedirs(log_path, exist_ok=True)
        if env.config.git_management:
            GitToolRepositoryImpl.create_gitignore(workspace)
            FileToolRepositoryImpl.update_file(
                os.path.join(workspace, ".gitignore"), "logs/"
            )
            GitToolRepositoryImpl.git_init(workspace)
            GitToolRepositoryImpl.git_add(workspace)
            GitToolRepositoryImpl.git_commit(workspace, f"Initial commit")

    # TODO clean directory(pycache, etc.)
    def postprocessing(self):
        pass

    @staticmethod
    def save_chain(
        file_path: str,
        global_env: ChatEnvRepositoryImpl,
        phase_name: str,
        phase_idx: int,
    ) -> None:
        phase_name = phase_name.replace("RepositoryImpl", "").replace("Phase", "")
        chain_dict = {"env": global_env, "phase": phase_name, "phase_idx": phase_idx}
        with open(file_path, "wb") as f:
            pickle.dump(chain_dict, f)
        print()
        print(f"\033[31mChain saved on {file_path}.\033[0m")

    @staticmethod
    def load_chain(file_path: str) -> Tuple[ChatEnvRepositoryImpl, str]:
        try:
            with open(file_path, "rb") as f:
                chain_dict = pickle.load(f)
        except Exception:
            raise TypeError(f"\033[31m`chain_path` is not provided.\033[0m")

        env = chain_dict["env"]
        phase = chain_dict["phase"]
        phase_idx = chain_dict["phase_idx"]
        print()
        print(
            f"\033[31mChain Loaded from {file_path}.\nStarting from [{phase}] phase...\033[0m"
        )
        return env, phase, phase_idx
