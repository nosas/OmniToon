from src.battle.attack import Attack


from dataclasses import dataclass


@dataclass
class CogAttack(Attack):
    # TODO: Add freq as an attribute

    def __repr__(self) -> str:
        return str(self.__dict__)