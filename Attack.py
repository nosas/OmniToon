from __future__ import annotations

from dataclasses import dataclass, field

from .AttackGlobals import Group


@dataclass
class Attack():

    name: str
    damage: int
    accuracy: int
    group: int = field(default=Group.Unknown)  # Multi or single-target attack
