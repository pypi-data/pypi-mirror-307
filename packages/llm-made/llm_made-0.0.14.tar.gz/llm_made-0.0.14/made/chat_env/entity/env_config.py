from dataclasses import dataclass


@dataclass
class EnvConfig:
    task_prompt: str
    directory: str
    background_prompt: str = (
        "SI-follow is a software company powered by LLM multi-agent"
    )
    clear_structure: bool = True
    incremental_develop: bool = False
    git_management: bool = False
    gui_design: bool = True
