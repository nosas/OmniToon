from dataclasses import dataclass, field

from .AttackGlobals import GROUP


@dataclass
class Attack():

    name: str
    damage: int
    accuracy: int
    group: int = field(default=GROUP.UNKNOWN)  # Multi or single-target attack
