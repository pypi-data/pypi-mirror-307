from dataclasses import dataclass


@dataclass
class RoleType:
    CEO: str = "Chief Executive Officer"
    CPO: str = "Chief Product Officer"
    CTO: str = "Chief Technology Officer"
    COUNSELOR: str = "Counselor"
    PROGRAMMER: str = "Programmer"
    REVIEWER: str = "Code Reviewer"
    TESTER: str = "Software Test Engineer"
