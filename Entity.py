from __future__ import annotations

from .Exceptions import InvalidTargetError


class Entity:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        # TODO Create Publisher object to push notifications

    def _get_attacked(self, amount: int):
        self.hp -= amount

    def do_attack(self, target: Entity, amount: int):
        type_self = type(self)
        type_target = type(target)

        # ! Raise InvalidTargetError if type(target) != Entity
        if not isinstance(target, Entity):
            raise InvalidTargetError

        # ! Raise InvalidTargetError if type(target) == type(self)
        if type(target) == type(self):
            raise InvalidTargetError

        # TODO Add chance_to_hit
        target._get_attacked(amount=amount)
        return 1

    def is_defeated(self):
        return self.hp <= 0
