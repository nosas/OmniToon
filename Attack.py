from dataclasses import dataclass, field


ATK_TGT_UNKNOWN, ATK_TGT_SINGLE, ATK_TGT_MULTI = (0, 1, 2)  # previously 1,2,3


@dataclass
class Attack():

    name: str
    damage: int
    accuracy: int
    target: int = field(default=ATK_TGT_UNKNOWN)  # Multi or single-target
