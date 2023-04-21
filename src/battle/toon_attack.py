from dataclasses import dataclass, field

from src.gags.gag import Gag

from .attack import Attack
from .attack_globals import GROUP


@dataclass
class ToonAttack(Attack):
    gag: Gag

    name: str = field(init=False)
    damage: int = field(init=False)
    accuracy: int = field(init=False)
    group: GROUP = field(init=False)

    # Trap-specific attributes used for tracking EXP rewards
    _is_attack: bool = field(default=False, repr=False)
    _is_setup: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.weight = self.gag.level

        super().__init__(
            name=self.gag.name,
            damage=self.gag.damage,
            accuracy=self.gag.accuracy,
            group=self.gag.target,
        )

    @property
    def reward(self) -> float:
        reward = self.gag.level + 1
        return max(-1, reward)

    @property
    def is_attack(self) -> bool:
        return self._is_attack

    @is_attack.setter
    def is_attack(self, new_is_attack: bool) -> None:
        assert isinstance(new_is_attack, bool)

        print(
            f"                [>] is_attack : {self.is_attack} -> {new_is_attack} on {self}"
        )  # noqa
        self._is_attack = new_is_attack

    @property
    def is_setup(self) -> bool:
        return self._is_setup

    @is_setup.setter
    def is_setup(self, new_is_setup: bool) -> None:
        assert isinstance(new_is_setup, bool)
        print(
            f"                [>] is_setup : {self.is_setup} -> {new_is_setup} on {self}"
        )  # noqa
        self._is_setup = new_is_setup
