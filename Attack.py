from __future__ import annotations

from dataclasses import dataclass, field

from .AttackGlobals import ATK_TGT_UNKNOWN


@dataclass
class Attack():

    name: str
    damage: int
    accuracy: int
    group: int = field(default=ATK_TGT_UNKNOWN)  # Multi or single-target attack
