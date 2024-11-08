from dataclasses import dataclass
from typing import Dict, Optional

from made.messages.entity.base_message import BaseMessage


@dataclass
class BaseSystemMessage(BaseMessage):
    role_name: str
    meta_dict: Optional[Dict[str, str]] = None
    role: str = "system"
    content: str = ""
