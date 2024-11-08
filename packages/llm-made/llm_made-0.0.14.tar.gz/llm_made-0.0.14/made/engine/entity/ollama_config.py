from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class OllamaConfig:
    base_url: str = "http://127.0.0.1:11434/v1/"
    model: str = "llama3.2"
    api_key: str = "ollama"
    max_tokens: int = 40000
    stream: bool = False
    temperature: float = 1.0
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: Optional[Union[str, List[str]]] = None
    seed: Optional[int] = None
