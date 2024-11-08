from dataclasses import dataclass
from typing import Optional, Dict

from made.messages.entity.chat_message.base_chat_message import BaseChatMessage


@dataclass
class UserChatMessage(BaseChatMessage):
    role_name: str = "user"
    meta_dict: Optional[Dict[str, str]] = None
    role: str = "user"
    content: str = ""
