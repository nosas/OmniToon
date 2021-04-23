from __future__ import annotations

from .Attack import Attack
from .Exceptions import InvalidTargetError, TargetDefeatedError


class Entity:
    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp
        # TODO #25, Create Publisher object to push notifications

    @property
    def is_defeated(self):
        return self.hp <= 0

    def _get_attacked(self, amount: int):
        self.hp -= amount

    def choose_attack():
        raise NotImplementedError

    def do_attack(self, target: Entity, attack: Attack,
                  overdefeat: bool = False, force_miss: bool = False) -> int:
        if not isinstance(target, Entity):
            raise InvalidTargetError("Target must be a subclass of Entity")
        if type(target) == type(self):
            raise InvalidTargetError("Target must not be of the same type")

        if target.is_defeated and overdefeat is False:
            # Multiple Toons attack the same Cog with the same Gag track
            raise TargetDefeatedError(f"Cannot attack defeated {type(target)}")

        target_hp_before = target.hp

        # TODO #10, Add chance_to_hit
        attack_hit = False if force_miss else True
        hit_miss = 'hits' if attack_hit else 'misses'
        damage = attack.damage if attack_hit else 0
        target._get_attacked(amount=damage)

        class_name = self.__class__.__name__
        # TODO Add attack name and object name
        print(f"            [-] {class_name} `do_attack()` {self} "
              f"{attack.name} {hit_miss} {target} -> {target_hp_before}hp-"
              f"{damage}dmg")
        return attack_hit
