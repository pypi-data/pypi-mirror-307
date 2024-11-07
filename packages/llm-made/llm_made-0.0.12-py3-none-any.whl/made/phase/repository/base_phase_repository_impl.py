import os
from copy import deepcopy
from typing import Dict, Optional, Union

from made.agent.service.agent_service_impl import AgentServiceImpl
from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from made.engine import ModelConfig
from made.messages.entity.chat_message.user_message import UserChatMessage
from made.messages.entity.system_message.assistant_system_message import (
    AssistantSystemMessage,
)
from made.phase.entity.phase_states import PhaseStates
from made.phase.repository.base_phase_repository import BasePhaseRepository
from made.role_playing.service.role_playing_service_impl import RolePlayingServiceImpl
from made.tools.rag.repository.rag_tool_repository_impl import RAGToolRepositoryImpl
from made.utils.logger import Logger


class BasePhaseRepositoryImpl(BasePhaseRepository):
    def __init__(
        self,
        model_config: ModelConfig,
        phase_prompt: str,
        assistant_role_name: str,
        assistant_role_prompt: str,
        user_role_name: str,
        user_role_prompt: str,
        chat_turn_limit: int = 10,
        conversation_rag: bool = False,
        conversation_logging: bool = True,
        **kwargs,
    ):
        model_config = deepcopy(model_config)
        self.model_config = model_config
        if temperature := kwargs.get("temperature"):
            if temperature is not None:
                self.model_config.temperature = temperature
        if top_p := kwargs.get("top_p"):
            if top_p is not None:
                self.model_config.top_p = top_p
        self.phase_prompt = phase_prompt
        self.assistant_role_name = assistant_role_name
        self.assistant_role_prompt = assistant_role_prompt
        self.user_role_name = user_role_name
        self.user_role_prompt = user_role_prompt
        self.chat_turn_limit = chat_turn_limit
        self.conversation_rag = conversation_rag
        self.conversation_logging = conversation_logging

        self.seminar_conclusion = None

        states = kwargs.get("states")
        self.states: Optional[Union[PhaseStates, Dict]] = (
            states if states else PhaseStates()
        )

    def chatting(
        self,
        env: ChatEnvRepositoryImpl,
        task_prompt: str,
        phase_prompt: str,
        assistant_role_name: str,
        assistant_role_prompt: str,
        user_role_name: str,
        user_role_prompt: str,
        placeholders=None,
        chat_turn_limit=10,
    ) -> str:
        if placeholders is None:
            placeholders = {}
        if not isinstance(placeholders, dict):
            placeholders = placeholders.__dict__
        assert 1 <= chat_turn_limit <= 100

        conversation_logger = None
        if self.conversation_logging:
            conversation_logger = Logger(
                f"{__class__.__name__}_{env.config.directory}",
                os.path.join(
                    env.config.directory, "logs", f"{ self.__class__.__name__}.log"
                ),
            ).get_logger()

        role_play_session = RolePlayingServiceImpl(
            model_config=self.model_config,
            task_prompt=task_prompt,
            assistant_role_name=assistant_role_name,
            assistant_role_prompt=assistant_role_prompt,
            user_role_name=user_role_name,
            user_role_prompt=user_role_prompt,
            background_prompt=env.config.background_prompt,
        )

        _, input_user_message = role_play_session.role_playing_repository.init_chat(
            placeholders, phase_prompt
        )
        # print()
        # print(
        #     f"\033[93m{input_user_message.role_name}\033[0m",
        #     ": ",
        #     input_user_message.content,
        # )
        if conversation_logger is not None:
            conversation_logger.info(
                f"{input_user_message.role_name}: {input_user_message.content}"
            )
        seminar_conclusion = None

        for _ in range(chat_turn_limit):
            assistant_response, user_response = role_play_session.step(
                input_user_message, chat_turn_limit == 1
            )
            # print()
            # print(
            #     f"\033[93m{assistant_response.message.role_name}\033[0m",
            #     ": ",
            #     assistant_response.message.content,
            # )
            if conversation_logger is not None:
                conversation_logger.info(
                    f"{assistant_response.message.role_name}: {assistant_response.message.content}"
                )
            if user_response.message is not None:
                # print()
                # print(
                #     f"\033[93m{user_response.message.role_name}\033[0m",
                #     ": ",
                #     user_response.message.content,
                # )
                if conversation_logger is not None:
                    conversation_logger.info(
                        f"{user_response.message.role_name}: {user_response.message.content}"
                    )
            if (
                role_play_session.role_playing_repository.assistant_agent.agent_repository.info
            ):
                seminar_conclusion = assistant_response.message.content
                break
            if assistant_response.terminated:
                break

            if (
                role_play_session.role_playing_repository.user_agent.agent_repository.info
            ):
                seminar_conclusion = user_response.message.content
                break
            if user_response.terminated:
                break

            if chat_turn_limit > 1:
                input_user_message = user_response.message
            else:
                break

        # TODO seminar conclusion should be more clear
        if seminar_conclusion is None:
            if self.conversation_rag:
                conversations = (
                    role_play_session.role_playing_repository.assistant_agent.agent_repository.stored_messages
                )
                task = conversations[0].content
                conversations = [
                    conversation.content for conversation in conversations[1:]
                ]
                client = RAGToolRepositoryImpl.get_client(
                    os.path.join(env.config.directory, "vectordb")
                )
                collection = RAGToolRepositoryImpl.get_collection(
                    client, "conversations"
                )
                RAGToolRepositoryImpl.ingest(
                    collection, conversations, self.model_config
                )
                search_result = RAGToolRepositoryImpl.search(
                    task, collection, self.model_config, n_results=2
                )
                rag_prompt = (
                    f"Query search result: {search_result}\n"
                    + f"Using the result, do {task}."
                )
                message = UserChatMessage(content=task)
                agent = AgentServiceImpl(
                    system_message=AssistantSystemMessage(
                        role_name=assistant_role_name, content=rag_prompt
                    ),
                    model_config=self.model_config,
                )
                seminar_conclusion = agent.step(message).message.content
                if "<INFO>" not in seminar_conclusion:
                    seminar_conclusion = "<INFO>" + seminar_conclusion
            else:
                seminar_conclusion = "<INFO>" + assistant_response.message.content

        seminar_conclusion = seminar_conclusion.split("<INFO>")[-1]
        # print()
        # print(f"\033[31mseminar conclusion\033[0m: {seminar_conclusion}")
        if conversation_logger is not None:
            conversation_logger.info(f"[seminar conclusion]: {seminar_conclusion}")
        return seminar_conclusion

    def update_phase_states(self, env: ChatEnvRepositoryImpl):
        """
        Update the phase states from previous phases states(global env).

        Args:
            env (ChatEnvRepositoryImpl): The chat environment.
        """
        raise NotImplementedError

    def update_env_states(self, env: ChatEnvRepositoryImpl):
        """
        Update the environment states based on the seminar conclusion.

        Args:
            env (ChatEnvRepositoryImpl): The chat environment.
        """
        raise NotImplementedError

    def execute(
        self,
        env: ChatEnvRepositoryImpl,
    ) -> ChatEnvRepositoryImpl:
        self.update_phase_states(env)
        self.seminar_conclusion = self.chatting(
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
        env = self.update_env_states(env)
        return env
