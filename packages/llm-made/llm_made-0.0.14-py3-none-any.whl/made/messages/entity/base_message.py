from dataclasses import dataclass
from typing import Any, Dict, Optional, Union


@dataclass
class BaseMessage:
    role_name: str
    meta_dict: Optional[Dict[str, str]]
    role: str
    content: str
    function_call: Any = None
    tool_calls: Any = None

    def __getattribute__(self, name: str) -> Any:
        delegate_methods = [method for method in dir(str) if not method.startswith("_")]
        if name in delegate_methods:
            content = super().__getattribute__("content")
            if isinstance(content, str):
                content_method = getattr(content, name, None)
                if callable(content_method):

                    def modify_arg(arg: Any) -> Any:
                        if isinstance(arg, BaseMessage):
                            return arg.content
                        elif isinstance(arg, (list, tuple)):
                            return type(arg)(modify_arg(item) for item in arg)
                        else:
                            return arg

                    def wrapper(*args: Any, **kwargs: Any) -> Any:
                        modified_args = [modify_arg(arg) for arg in args]
                        modified_kwargs = {k: modify_arg(v) for k, v in kwargs.items()}
                        output = content_method(*modified_args, **modified_kwargs)
                        return (
                            self._create_new_instance(output)
                            if isinstance(output, str)
                            else output
                        )

                    return wrapper

        return super().__getattribute__(name)

    def _create_new_instance(self, content: str) -> "BaseMessage":
        return self.__class__(
            role_name=self.role_name,
            meta_dict=self.meta_dict,
            role=self.role,
            content=content,
        )

    def __add__(self, other: Any) -> Union["BaseMessage", Any]:
        if isinstance(other, BaseMessage):
            combined_content = self.content.__add__(other.content)
        elif isinstance(other, str):
            combined_content = self.content.__add__(other)
        else:
            raise TypeError(
                f"Unsupported operand type(s) for +: '{type(self)}' and "
                f"'{type(other)}'"
            )
        return self._create_new_instance(combined_content)

    def __mul__(self, other: Any) -> Union["BaseMessage", Any]:
        if isinstance(other, int):
            multiplied_content = self.content.__mul__(other)
            return self._create_new_instance(multiplied_content)
        else:
            raise TypeError(
                f"Unsupported operand type(s) for *: '{type(self)}' and "
                f"'{type(other)}'"
            )

    def __len__(self) -> int:
        return len(self.content)

    def __contains__(self, item: str) -> bool:
        return item in self.content

    def to_message(self, role: Optional[str] = None) -> Dict[str, str]:
        role = role or self.role
        if role not in {"system", "user", "assistant"}:
            raise ValueError(f"Unrecognized role: {role}")
        return {"role": role, "content": self.content}

    def to_chat_message(
        self,
        role: Optional[str] = None,
    ) -> Dict[str, str]:
        role = role or self.role
        if role not in {"user", "assistant"}:
            raise ValueError(f"Unrecognized role: {role}")
        return {"role": role, "content": self.content}

    def to_system_message(self) -> Dict[str, str]:
        return {"role": "system", "content": self.content}

    def to_user_message(self) -> Dict[str, str]:
        return {"role": "user", "content": self.content}

    def to_assistant_message(self) -> Dict[str, str]:
        return {"role": "assistant", "content": self.content}
