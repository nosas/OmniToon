from typing import Type

import pytest
from pytest import FixtureRequest

from src.battle.attack_globals import MULTIPLIER
from src.battle.battle import Battle, BattleToon
from src.core.toon import Toon
from src.factories.utils import create_battle_cog, create_random_cog

from ..utils.utils import get_cog_from_request_param


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
def bc(request: Type[FixtureRequest]):
    """Return a BattleCog with battle_id == 1"""
    return create_battle_cog(battle_id=0, entity=request.param)


@pytest.fixture
def bc_random():
    """Return a random BattleCog with battle_id == 1"""
    return create_battle_cog(battle_id=0, entity=create_random_cog())


@pytest.fixture
def bc_random_lured():
    """Return a random, lured BattleCog with battle_id == 1"""
    return create_battle_cog(battle_id=0, entity=create_random_cog(), lured=True)


@pytest.fixture
def bc_random_trapped():
    """Return a random, trapped BattleCog with battle_id == 1"""
    return create_battle_cog(battle_id=0, entity=create_random_cog(), trapped=True)


@pytest.fixture
def bc_lured(request: Type[FixtureRequest]):
    """Given a Cog object, or a (key, rel_lvl) tuple, return a lured BattleCog

    Args:
        cog (Cog): Cog object
        key_rel_lvl (Tuple[str, int]): Cog's key and relative_level in a tuple

    Returns:
        BattleCog: A lured BattleCog
    """
    return create_battle_cog(
        battle_id=0, entity=get_cog_from_request_param(request.param), lured=True
    )


@pytest.fixture
def bc_trapped(request: Type[FixtureRequest]):
    """Given a Cog object, or a (key, rel_lvl) tuple, return a trapped BattleCog

    Args:
        cog (Cog): Cog object
        key_rel_lvl (Tuple[str, int]): Cog's key and relative_level in a tuple

    Returns:
        BattleCog: A trapped BattleCog
    """
    return create_battle_cog(
        battle_id=0, entity=get_cog_from_request_param(request.param), trapped=True
    )


@pytest.fixture(params=[1, 2, 3, 4, 5], scope="module")
def building_floor(request: Type[FixtureRequest]) -> int:
    """Return all possible building floor values, one at a time"""
    return request.param


@pytest.fixture(scope="module")
def expected_building_multiplier(building_floor: int) -> float:
    """Given a building_floor value, return the expected building_multiplier value"""
    return MULTIPLIER.get_building_multiplier_from_floor(floor=building_floor)
