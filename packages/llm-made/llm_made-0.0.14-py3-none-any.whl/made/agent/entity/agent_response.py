from dataclasses import dataclass
from typing import Any, Dict, List

from made.messages.entity.chat_message.base_chat_message import BaseChatMessage


@dataclass(frozen=True)
class ChatAgentResponse:
    messages: List[BaseChatMessage]
    terminated: bool
    info: Dict[str, Any]

    @property
    def message(self):
        if self.terminated:
            raise RuntimeError("error in AgentResponse, info:{}".format(str(self.info)))
        if len(self.messages) > 1:
            raise RuntimeError(
                "Property message is only available for a single message in messages"
            )
        elif len(self.messages) == 0:
            if len(self.info) > 0:
                raise RuntimeError(
                    "Empty messages in AgentResponse, info:{}".format(str(self.info))
                )
            else:
                return None
        return self.messages[0]
