from typing import Any, Dict, List, Optional, Union

from made.agent.repository.agent_repository import AgentRepository
from made.engine import ModelConfig
from made.engine.service.ollama.ollama_engine_service_impl import OllamaEngineServiceImpl
from made.messages import MessageType
from made.messages.entity.chat_message.base_chat_message import BaseChatMessage
from made.messages.entity.system_message.base_system_message import BaseSystemMessage


class AgentRepositoryImpl(AgentRepository):
    def __init__(
        self,
        system_message: BaseSystemMessage,
        model_config: ModelConfig,
        message_window_size: Optional[int] = None,
    ) -> None:
        self.system_message: BaseSystemMessage = system_message
        self.role_name: str = system_message.role_name
        self.engine: Union[OllamaEngineServiceImpl] = (
            OllamaEngineServiceImpl.get_instance()
        )
        self.model_config: ModelConfig = model_config
        self.model_token_limit: int = model_config.max_tokens
        self.message_window_size: Optional[int] = message_window_size
        self.terminated: bool = False
        self.info: bool = False
        self.init_messages()

    def reset(self) -> List[MessageType]:
        self.terminated = False
        self.init_messages()
        return self.stored_messages

    def get_info(
        self,
        id: Optional[str],
        usage: Optional[Dict[str, int]],
        termination_reasons: List[str],
        num_tokens: int,
    ) -> Dict[str, Any]:
        return {
            "id": id,
            "usage": usage,
            "termination_reasons": termination_reasons,
            "num_tokens": num_tokens,
        }

    def init_messages(self) -> None:
        self.stored_messages: List[MessageType] = [self.system_message]

    def update_messages(self, message: BaseChatMessage) -> List[MessageType]:
        self.stored_messages.append(message)
        return self.stored_messages
