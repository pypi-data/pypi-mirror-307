from made.chat_env.entity.env_config import EnvConfig
from made.chat_env.entity.env_states import EnvStates
from made.chat_env.repository.chat_env_repository import ChatEnvRepository


class ChatEnvRepositoryImpl(ChatEnvRepository):
    def __init__(self, env_config: EnvConfig, env_states: EnvStates = EnvStates()):
        self.reset(env_config, env_states)

    def reset(self, env_config: EnvConfig, env_states: EnvStates = EnvStates()):
        self.config = env_config
        self.states = env_states
