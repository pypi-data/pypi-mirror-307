from typing import Dict, List, Optional, Tuple

from made.agent.entity.agent_response import ChatAgentResponse
from made.engine import ModelConfig
from made.messages.entity.chat_message.base_chat_message import BaseChatMessage
from made.role_playing.repository.role_playing_repository_impl import (
    RolePlayingRepositoryImpl,
)
from made.role_playing.service.role_playing_service import RolePlayingService


class RolePlayingServiceImpl(RolePlayingService):
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
    ):
        self.role_playing_repository = RolePlayingRepositoryImpl(
            model_config=model_config,
            task_prompt=task_prompt,
            assistant_role_name=assistant_role_name,
            assistant_role_prompt=assistant_role_prompt,
            user_role_name=user_role_name,
            user_role_prompt=user_role_prompt,
            assistant_agent_kwargs=assistant_agent_kwargs,
            user_agent_kwargs=user_agent_kwargs,
            extend_system_message_meta_dicts=extend_system_message_meta_dicts,
            background_prompt=background_prompt,
        )

    def step(
        self,
        user_message: BaseChatMessage,
        assistant_only: bool,
    ) -> Tuple[ChatAgentResponse, ChatAgentResponse]:
        assert isinstance(user_message, BaseChatMessage), print(
            "broken user_message: " + str(user_message)
        )

        user_message_set_role = user_message.set_user_role()
        assistant_response = self.role_playing_repository.assistant_agent.step(
            user_message_set_role
        )
        if assistant_response.terminated or assistant_response.messages is None:
            return (
                ChatAgentResponse(
                    [assistant_response.messages],
                    assistant_response.terminated,
                    assistant_response.info,
                ),
                ChatAgentResponse([], False, {}),
            )
        assistant_message = self.role_playing_repository.process_messages(
            assistant_response.messages
        )
        if self.role_playing_repository.assistant_agent.agent_repository.info:
            return (
                ChatAgentResponse(
                    [assistant_message],
                    assistant_response.terminated,
                    assistant_response.info,
                ),
                ChatAgentResponse([], False, {}),
            )
        self.role_playing_repository.assistant_agent.agent_repository.update_messages(
            assistant_message
        )

        if assistant_only:
            return (
                ChatAgentResponse(
                    [assistant_message],
                    assistant_response.terminated,
                    assistant_response.info,
                ),
                ChatAgentResponse([], False, {}),
            )

        assistant_message_set_role = assistant_message.set_user_role()
        user_response = self.role_playing_repository.user_agent.step(
            assistant_message_set_role
        )
        if user_response.terminated or user_response.messages is None:
            return (
                ChatAgentResponse(
                    [assistant_message],
                    assistant_response.terminated,
                    assistant_response.info,
                ),
                ChatAgentResponse(
                    [user_response], user_response.terminated, user_response.info
                ),
            )
        user_message = self.role_playing_repository.process_messages(
            user_response.messages
        )
        if self.role_playing_repository.user_agent.agent_repository.info:
            return (
                ChatAgentResponse(
                    [assistant_message],
                    assistant_response.terminated,
                    assistant_response.info,
                ),
                ChatAgentResponse(
                    [user_message], user_response.terminated, user_response.info
                ),
            )
        self.role_playing_repository.user_agent.agent_repository.update_messages(
            user_message
        )

        return (
            ChatAgentResponse(
                [assistant_message],
                assistant_response.terminated,
                assistant_response.info,
            ),
            ChatAgentResponse(
                [user_message], user_response.terminated, user_response.info
            ),
        )
