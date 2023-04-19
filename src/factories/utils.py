from src.battle.battle import RewardCalculator
from src.core.cog import Cog
from src.core.entity import Entity
from src.gags.gag import Gag

from .factory import (
    BattleCogFactory,
    BattleEntityFactory,
    CogFactory,
    EntityFactory,
    GagFactory,
    RandomCogFactory,
    ToonAttackFactory,
)


def create_toon_attack(gag: Gag, target_cog: Cog) -> Gag:
    return ToonAttackFactory().create_toon_attack(gag=gag, target_cog=target_cog)


def create_gag(track: str, level: int = 0, exp: int = 0, count: int = 0) -> Gag:
    return GagFactory().create_gag(track=track, level=level, exp=exp, count=count)


def create_cog(key: str = None, relative_level: int = 0) -> Cog:
    return CogFactory().create_cog(key=key, relative_level=relative_level)


def create_random_cog(key: str = None, relative_level: int = None) -> Cog:
    return RandomCogFactory().create_cog(key=key, relative_level=relative_level)


def create_battle_cog(
    battle_id: int, entity: Cog, lured: bool = False, trapped: bool = False
) -> Cog:
    return BattleCogFactory().create_battle_cog(
        battle_id=battle_id, entity=entity, lured=lured, trapped=trapped
    )


def create_battle_entity(battle_id: int, entity: Cog) -> Cog:
    return BattleEntityFactory().create_battle_entity(
        battle_id=battle_id, entity=entity
    )


def create_entity(name: str, hp: int) -> Entity:
    return EntityFactory().create_entity(name=name, hp=hp)


def create_reward_calculator(
    building_floor: int = 1, is_invasion: bool = False
) -> RewardCalculator:
    """Return a RewardCalculator, given a building_floor number and is_invasion boolean"""
    return RewardCalculator(building_floor=building_floor, is_invasion=is_invasion)
