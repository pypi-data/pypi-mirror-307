import os
from typing import List, Optional

from made.chat_chain.repository.chat_chain_repository_impl import (
    ChatChainRepositoryImpl,
)
from made.chat_chain.service.chat_chain_service import ChatChainService
from made.chat_env.entity.env_config import EnvConfig
from made.chat_env.entity.env_states import EnvStates
from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from made.engine.entity.ollama_config import OllamaConfig
from made.phase.service.phase_service_impl import PhaseServiceImpl


class ChatChainServiceImpl(ChatChainService):
    def __init__(
        self,
        task_prompt: str,
        directory: str,
        phases: List[str] = [
            "DefaultDemandAnalysis",
            "DefaultLanguageChoose",
            "DefaultCoding",
            "DefaultCodeComplete",
            "DefaultCodeReviewComment",
            "DefaultCodeReviewModification",
            "DefaultTestErrorSummary",
            "DefaultTestModification",
            "DefaultManual",
        ],
        base_url: str = "http://127.0.0.1:11434/v1/",
        model: str = "llama3.2",
        api_key: str = "ollama",
        max_tokens: int = 40000,
        git_management: bool = False,
        save_chain: bool = False,
        save_name: Optional[str] = "chain",
        env_states: EnvStates = EnvStates(),
        **kwargs,
    ):
        self.model_config = OllamaConfig(
            base_url=base_url, model=model, api_key=api_key, max_tokens=max_tokens
        )
        self.chat_chain_repository = ChatChainRepositoryImpl()
        self.phase_service = PhaseServiceImpl(
            model_config=self.model_config,
        )

        env_config = EnvConfig(
            task_prompt=task_prompt, directory=directory, git_management=git_management
        )

        self.env = ChatEnvRepositoryImpl(env_config=env_config, env_states=env_states)
        self.save_chain = save_chain
        self.chain_path = os.path.join(directory, f"{save_name}.pkl")
        self.load_chain = os.path.exists(self.chain_path)
        self.phase_idx = -1
        if self.load_chain:
            env, last_phase, self.phase_idx = ChatChainRepositoryImpl.load_chain(self.chain_path)
            self.env = env
            self.phases = self.get_phases(phases[self.phase_idx+1:])
        else:
            self.phases = self.get_phases(phases)

    def get_phases(self, phases: List[str]):
        phases = [self.phase_service.get_phase(phase) for phase in phases]
        return phases

    def run(self):
        if not self.load_chain:
            self.chat_chain_repository.preprocessing(self.env)
        self.chat_chain_repository.execute_chain(
            env=self.env,
            phases=self.phases,
            save_chain=self.save_chain,
            file_path=self.chain_path,
            phase_idx=self.phase_idx
        )
        self.chat_chain_repository.postprocessing()
