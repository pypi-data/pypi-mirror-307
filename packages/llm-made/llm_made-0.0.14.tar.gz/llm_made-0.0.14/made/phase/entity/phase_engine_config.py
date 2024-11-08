from dataclasses import dataclass


@dataclass
class EngineParams:
    temperature: float = 1.0
    top_p: float = 1.0


@dataclass
class PhaseEngineConfig:
    demand_analysis: EngineParams = EngineParams(temperature=0.7, top_p=0.8)
    language_choose: EngineParams = EngineParams(temperature=0.3, top_p=0.1)
    coding: EngineParams = EngineParams(temperature=0.2, top_p=0.1)
    code_complete: EngineParams = EngineParams(temperature=0.1, top_p=0.1)
    code_review_comment: EngineParams = EngineParams(temperature=0.1, top_p=0.1)
    code_review_modification: EngineParams = EngineParams(temperature=0.2, top_p=0.1)
    test_error_summary: EngineParams = EngineParams(temperature=0.1, top_p=0.1)
    test_modification: EngineParams = EngineParams(temperature=0.1, top_p=0.1)
    manual: EngineParams = EngineParams(temperature=0.7, top_p=0.4)
