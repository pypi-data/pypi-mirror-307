from typing import Any, Dict, List, Optional

from tenacity import retry, stop_after_attempt, wait_exponential

from made.agent.entity.agent_response import ChatAgentResponse
from made.agent.repository.agent_repository_impl import AgentRepositoryImpl
from made.agent.service.agent_service import Agentservice
from made.engine import ModelConfig
from made.messages.entity.chat_message.base_chat_message import BaseChatMessage
from made.messages.entity.system_message.base_system_message import BaseSystemMessage


class AgentServiceImpl(Agentservice):
    def __init__(
        self,
        system_message: BaseSystemMessage,
        model_config: ModelConfig,
        message_window_size: int = None,
    ):
        self.agent_repository = AgentRepositoryImpl(
            system_message, model_config, message_window_size
        )
        self.terminated = False

    @retry(wait=wait_exponential(min=5, max=60), stop=stop_after_attempt(5))
    def step(
        self,
        input_message: BaseChatMessage,
    ) -> ChatAgentResponse:
        messages = self.agent_repository.update_messages(input_message)
        if (
            self.agent_repository.message_window_size is not None
            and len(messages) > self.agent_repository.message_window_size
        ):
            messages = [self.agent_repository.system_message] + messages[
                -self.agent_repository.message_window_size :
            ]
        messages = [message.to_message() for message in messages]

        try:
            response = self.agent_repository.engine.chat_completion(
                messages=messages, ollama_config=self.agent_repository.model_config
            )
            output_messages = [
                BaseChatMessage(
                    role_name=self.agent_repository.role_name,
                    meta_dict=dict(),
                    **dict(choice.message),
                )
                for choice in response.choices
            ]
            info = self.agent_repository.get_info(
                response.id,
                response.usage,
                [str(choice.finish_reason) for choice in response.choices],
                response.usage.total_tokens,
            )

            if output_messages[0].content.split("\n")[-1].startswith("<INFO>"):
                self.agent_repository.info = True

        except Exception as e:
            print(f"error occurred: {e}")
            self.terminated = True
            output_messages = []

            info = self.agent_repository.get_info(
                None,
                None,
                ["max_tokens_exceeded"],
                response.usage.total_tokens,
            )

        return ChatAgentResponse(output_messages, self.terminated, info)
