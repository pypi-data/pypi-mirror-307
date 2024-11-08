from dataclasses import dataclass
from typing import Dict, Optional, Any

from made.messages.entity.base_message import BaseMessage


@dataclass
class BaseChatMessage(BaseMessage):
    role_name: str
    meta_dict: Optional[Dict[str, str]]
    role: str
    content: str = ""
    refusal: str = None

    def set_user_role(self: BaseMessage):
        return self.__class__(
            role_name=self.role_name,
            meta_dict=self.meta_dict,
            role="user",
            content=self.content,
        )
