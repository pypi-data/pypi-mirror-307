from dataclasses import dataclass
from typing import Dict, Optional

from made.messages.entity.system_message.base_system_message import BaseSystemMessage


@dataclass
class UserSystemMessage(BaseSystemMessage):
    role_name: str = "user"
    meta_dict: Optional[Dict[str, str]] = None
    role: str = "system"
    content: str = ""
