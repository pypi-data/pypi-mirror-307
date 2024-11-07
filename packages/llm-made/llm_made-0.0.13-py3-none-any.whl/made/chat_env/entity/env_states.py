from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class EnvStates:
    task_description: str = ""
    modality: str = ""
    ideas: str = ""
    language: str = ""
    review_comments: List[str] = field(default_factory=list)
    error_summary: List[str] = field(default_factory=list)
    test_reports: List[str] = field(default_factory=list)
    codes: Dict[str, str] = field(default_factory=dict)
    manual: Dict[str, str] = field(default_factory=dict)
    requirements: Dict[str, str] = field(default_factory=dict)
