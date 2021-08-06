import pytest

from ...AttackGlobals import MULTIPLIER
from ...Battle import Battle, BattleToon, RewardCalculator, ToonAttack
from ...Cog import Cog, get_random_cog
from ...Factory import BattleCogFactory
from ...Toon import Toon


@pytest.fixture
def battle_building(building_floor: int) -> Battle:
    return Battle(building_floor=building_floor)


@pytest.fixture
def battle_invasion() -> Battle:
    return Battle(is_invasion=True)


@pytest.fixture
def battle_building_invasion(building_floor: int) -> Battle:
    battle = Battle(building_floor=building_floor, is_invasion=True)
    return battle


@pytest.fixture
def bt_astro(toon_astro: Toon):
    bt_astro = BattleToon(battle_id=0, entity=toon_astro)
    return bt_astro


@pytest.fixture
def bt_trapa(toon_trapa: Toon):
    bt_trapa = BattleToon(battle_id=0, entity=toon_trapa)
    return bt_trapa


@pytest.fixture
def bc(request):
    """Return a BattleCog with battle_id == 1"""
    return BattleCogFactory.get_battle_cog(battle_id=0, entity=request.param)


@pytest.fixture
def bc_random():
    """Return a random BattleCog with battle_id == 1"""
    return BattleCogFactory.get_battle_cog(battle_id=0, entity=get_random_cog())


@pytest.fixture
def bc_random_lured():
    """Return a random, lured BattleCog with battle_id == 1"""
    return BattleCogFactory.get_battle_cog(battle_id=0, entity=get_random_cog(), lured=True)


@pytest.fixture
def bc_random_trapped():
    """Return a random, trapped BattleCog with battle_id == 1"""
    return BattleCogFactory.get_battle_cog(battle_id=0, entity=get_random_cog(), trapped=True)


@pytest.fixture
def bc_lured(request):
    """Given a Cog object, or a (key, rel_lvl) tuple, return a lured BattleCog

    Args:
        cog (Cog): Cog object
        key_rel_lvl (Tuple[str, int]): Cog's key and relative_level in a tuple

    Returns:
        BattleCog: A lured BattleCog
    """
    return BattleCogFactory.get_battle_cog(battle_id=0,
                                           entity=get_cog_from_request_param(request.param),
                                           lured=True)


@pytest.fixture
def bc_trapped(request):
    """Given a Cog object, or a (key, rel_lvl) tuple, return a trapped BattleCog

    Args:
        cog (Cog): Cog object
        key_rel_lvl (Tuple[str, int]): Cog's key and relative_level in a tuple

    Returns:
        BattleCog: A trapped BattleCog
    """
    return BattleCogFactory.get_battle_cog(battle_id=0,
                                           entity=get_cog_from_request_param(request.param),
                                           trapped=True)


@pytest.fixture(params=[1, 2, 3, 4, 5], scope='module')
def building_floor(request) -> int:
    """Return all possible building floor values, one at a time"""
    return request.param


@pytest.fixture(scope='module')
def expected_building_multiplier(building_floor: int) -> float:
    """Given a building_floor value, return the expected building_multiplier value"""
    return MULTIPLIER.get_building_multiplier_from_floor(floor=building_floor)


def get_cog_from_request_param(request_param) -> Cog:
    """Given a pytest request containing a Cog or a (key, rel_lvl) tuple, return a Cog object

    Args:
        request_param (Cog | Tuple[str, int]): Cog object or a (key, rel_lvl) tuple

    Returns:
        Cog: Cog object
    """
    if isinstance(request_param, tuple):
        return Cog(key=request_param[0], relative_level=request_param[1])
    elif isinstance(request_param, Cog):
        return request_param
    else:
        raise TypeError(f"What the heck did you request? {request_param}")


def get_expected_reward(toon_attack: ToonAttack, rc: RewardCalculator) -> int:
    """Given a ToonAttack and RewardCalculator, return the expected reward value"""
    if toon_attack.gag.level >= toon_attack.target_cog.level:
        return -1
    else:
        return round(rc.get_base_reward(attack=toon_attack) * rc.get_multiplier())


def get_reward_calculator(building_floor: int = 1, is_invasion: bool = False) -> RewardCalculator:
    """Return a RewardCalculator, given a building_floor number and is_invasion boolean"""
    return RewardCalculator(building_floor=building_floor, is_invasion=is_invasion)
