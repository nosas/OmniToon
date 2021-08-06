from abc import ABC
from dataclasses import dataclass


@dataclass
class Attack(ABC):

    name: str
    damage: int
    accuracy: int
    group: int  # Multi or single-target attack
