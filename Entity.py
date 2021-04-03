from __future__ import annotations

from .Exceptions import InvalidTargetError, TargetDefeatedError


class Entity:
    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp
        # TODO #25, Create Publisher object to push notifications

    def _get_attacked(self, amount: int):
        self.hp -= amount

    def choose_attack():
        raise NotImplementedError

    def do_attack(self, target: Entity, amount: int) -> int:

        if not isinstance(target, Entity):
            raise InvalidTargetError("Target must be a subclass of Entity")

        if type(target) == type(self):
            raise InvalidTargetError("Target must not be of the same type")

        if target.is_defeated():
            raise TargetDefeatedError("Target is defeated")

        target_hp_before = target.hp

        # TODO #10, Add chance_to_hit
        attack_hit = True
        hit_miss = 'hits' if attack_hit else 'misses'
        target._get_attacked(amount=amount)

        class_name = self.__class__.__name__
        print(f"        [-] {class_name} `do_attack` {hit_miss} : "
              f"{target_hp_before}hp-{amount if attack_hit else 0}dmg -> "
              f"{target}")
        return attack_hit

    def is_defeated(self):
        return self.hp <= 0
