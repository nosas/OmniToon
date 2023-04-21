from src.battle.toon_attack import ToonAttack
from src.gags.gag import Gag


class ToonAttackFactory:
    @staticmethod
    def create_toon_attack(gag: Gag):
        return ToonAttack(gag=gag)


def create_toon_attack(gag: Gag) -> Gag:
    return ToonAttackFactory().create_toon_attack(gag=gag)
