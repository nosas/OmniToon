from __future__ import annotations


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
        assert isinstance(target, Entity), (
            f"{type_self} {self.name} is attacking a non-Entity object"
        )

        # ! Raise InvalidTargetError if type(target) == type(self)
        assert type_self != type_target, (
            f"{type_self} {self.name} is attacking {type_target} {target.name}"
        )

        # TODO Add chance_to_hit
        target._get_attacked(amount=amount)
        return 1

    def get_name(self):
        return self.name

    def is_defeated(self):
        return self.hp <= 0
