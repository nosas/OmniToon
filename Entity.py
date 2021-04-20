from __future__ import annotations

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

    def do_attack(self, target: Entity, amount: int, overdefeat=False) -> int:
        if not isinstance(target, Entity):
            raise InvalidTargetError("Target must be a subclass of Entity")
        if type(target) == type(self):
            raise InvalidTargetError("Target must not be of the same type")
        if target.is_defeated:
            # Multiple Toons attack the same Cog with the same Gag track
            if overdefeat is True:
                pass
            raise TargetDefeatedError(f"Cannot attack defeated {type(target)}")

        target_hp_before = target.hp

        # TODO #10, Add chance_to_hit
        attack_hit = True
        hit_miss = 'hits' if attack_hit else 'misses'
        target._get_attacked(amount=amount)

        class_name = self.__class__.__name__
        # TODO Add attack name and object name
        print(f"            [-] {class_name} `do_attack()` {self} {hit_miss}"
              f" {target} -> {target_hp_before}hp-"
              f"{amount if attack_hit else 0}dmg")
        return attack_hit
