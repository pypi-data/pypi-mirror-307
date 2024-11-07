import copy
from typing import Dict, List, Optional, Sequence

from made.agent.service.agent_service_impl import AgentServiceImpl
from made.engine import ModelConfig
from made.messages.entity.chat_message.base_chat_message import BaseChatMessage
from made.messages.entity.chat_message.user_message import UserChatMessage
from made.messages.entity.system_message.assistant_system_message import (
    AssistantSystemMessage,
)
from made.messages.entity.system_message.user_system_message import UserSystemMessage
from made.role_playing.repository.role_playing_repository import RolePlayingRepository


class RolePlayingRepositoryImpl(RolePlayingRepository):
    def __init__(
        self,
        model_config: ModelConfig,
        task_prompt: str,
        assistant_role_name: str,
        assistant_role_prompt: str,
        user_role_name: str,
        user_role_prompt: str,
        assistant_agent_kwargs: Optional[Dict] = None,
        user_agent_kwargs: Optional[Dict] = None,
        extend_system_message_meta_dicts: Optional[List[Dict]] = None,
        background_prompt: Optional[str] = "",
    ) -> None:
        system_message_meta_dicts = [
            dict(background_prompt=background_prompt, task=task_prompt)
        ] * 2
        extend_system_message_meta_dicts = [
            dict(assistant_role=assistant_role_name, user_role=user_role_name)
        ] * 2
        if extend_system_message_meta_dicts is not None:
            system_message_meta_dicts = [
                {**system_message_meta_dict, **extend_system_message_meta_dict}
                for system_message_meta_dict, extend_system_message_meta_dict in zip(
                    system_message_meta_dicts, extend_system_message_meta_dicts
                )
            ]

        self.assistant_system_message = AssistantSystemMessage(
            role_name=assistant_role_name,
            meta_dict=system_message_meta_dicts[0],
            content=assistant_role_prompt.format(**system_message_meta_dicts[0]),
        )
        self.user_system_messsge = UserSystemMessage(
            role_name=user_role_name,
            meta_dict=system_message_meta_dicts[1],
            content=user_role_prompt.format(**system_message_meta_dicts[1]),
        )

        self.assistant_agent = AgentServiceImpl(
            system_message=self.assistant_system_message,
            model_config=model_config,
            **(assistant_agent_kwargs or {}),
        )
        self.user_agent = AgentServiceImpl(
            system_message=self.user_system_messsge,
            model_config=model_config,
            **(user_agent_kwargs or {}),
        )

    def init_chat(self, placeholders={}, phase_prompt=None):
        self.assistant_agent.agent_repository.reset()
        self.user_agent.agent_repository.reset()

        content = phase_prompt.format(
            **(
                {
                    "assistant_role": self.assistant_agent.agent_repository.role_name,
                    "user_role": self.user_agent.agent_repository.role_name,
                }
                | placeholders
            )
        )
        user_message = UserChatMessage(
            role_name=self.user_system_messsge.role_name, role="user", content=content
        )
        pseudo_message = copy.deepcopy(user_message)
        pseudo_message.role = "assistant"
        self.user_agent.agent_repository.update_messages(pseudo_message)

        return None, user_message

    def process_messages(
        self,
        messages: Sequence[BaseChatMessage],
    ) -> BaseChatMessage:
        if len(messages) == 0:
            raise ValueError("No messages to process.")
        if len(messages) > 1:
            raise ValueError(
                "Got more than one message to process. "
                f"Num of messages: {len(messages)}."
            )
        else:
            processed_message = messages[0]

        return processed_message
