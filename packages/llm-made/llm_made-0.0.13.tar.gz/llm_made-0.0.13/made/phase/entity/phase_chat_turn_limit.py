from dataclasses import dataclass


@dataclass
class PhaseChatTurnLimit:
    demand_analysis: int = 4
    language_choose: int = 4
    coding: int = 1
    code_complete: int = 1
    code_review_comment: int = 1
    code_review_modification: int = 1
    test_error_summary: int = 1
    test_modification: int = 1
    manual: int = 4
