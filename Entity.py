from __future__ import annotations

from .Exceptions import InvalidTargetError, TargetDefeatedError


class Entity:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        # TODO #25, Create Publisher object to push notifications

    def _get_attacked(self, amount: int):
        self.hp -= amount

    def do_attack(self, target: Entity, amount: int) -> int:

        if not isinstance(target, Entity):
            raise InvalidTargetError("Target must be a subclass of Entity")

        if type(target) == type(self):
            raise InvalidTargetError("Target must not be of the same type")

        if target.is_defeated():
            raise TargetDefeatedError("Target is defeated")

        # TODO #10, Add chance_to_hit
        target._get_attacked(amount=amount)
        return 1

    def is_defeated(self):
        return self.hp <= 0
