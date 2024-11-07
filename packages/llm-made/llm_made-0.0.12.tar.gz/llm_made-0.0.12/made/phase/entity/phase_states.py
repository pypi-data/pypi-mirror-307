from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class PhaseStates:
    task: str = ""
    description: str = ""
    modality: str = ""
    language: str = ""
    codes: Dict[str, str] = field(default_factory=dict)
    ideas: str = ""
    comments: str = ""
    review_comments: str = ""
    test_reports: str = ""
    exist_bugs_flag: bool = False
    error_summary: str = ""
    cycle_index: int = 1
    unimplemented_file: str = ""
    max_num_implement: int = 5
    num_tried: int = 0
    modification_conclusion: str = ""
    gui: bool = False
    code_files: List[str] = ""
    requirements: str = ""
