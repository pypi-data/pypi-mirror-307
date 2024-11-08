from typing import Union

from made.messages.entity.base_message import BaseMessage
from made.messages.entity.chat_message.assistant_message import AssistantChatMessage
from made.messages.entity.chat_message.base_chat_message import BaseChatMessage
from made.messages.entity.chat_message.user_message import UserChatMessage
from made.messages.entity.system_message.assistant_system_message import (
    AssistantSystemMessage,
)
from made.messages.entity.system_message.base_system_message import BaseSystemMessage
from made.messages.entity.system_message.user_system_message import UserSystemMessage


MessageType = Union[
    BaseMessage,
    AssistantChatMessage,
    BaseChatMessage,
    UserChatMessage,
    AssistantSystemMessage,
    BaseSystemMessage,
    UserSystemMessage,
]

SystemMessageType = Union[AssistantSystemMessage, BaseSystemMessage, UserSystemMessage]

ChatMessageType = Union[AssistantChatMessage, BaseChatMessage, UserChatMessage]
