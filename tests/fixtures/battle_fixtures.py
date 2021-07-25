import pytest

from ...Battle import BattleCog, BattleToon
from ...Cog import Cog, get_random_cog
from ...Toon import Toon


@pytest.fixture
def bt_astro(toon_astro: Toon):
    bt_astro = BattleToon(battle_id=1, entity=toon_astro)
    return bt_astro


@pytest.fixture
def bc_random_lured():
    """Return a random, lured BattleCog with battle_id == 1"""
    bc = BattleCog(battle_id=1, entity=get_random_cog())
    bc.is_lured = True
    return bc


@pytest.fixture
def bc_lured(request):
    """Given a Cog object, or a (key, rel_lvl) tuple, return a lured BattleCog

    Args:
        cog (Cog): Cog object
        key_rel_lvl (Tuple[str, int]): Cog's key and relative_level in a tuple

    Returns:
        BattleCog: A lured BattleCog
    """
    if isinstance(request.param, tuple):
        key, relative_level = request.param
        cog = Cog(key=key, relative_level=relative_level)
        bc = BattleCog(battle_id=1, entity=cog)
    elif isinstance(request.param, Cog):
        bc = BattleCog(battle_id=1, entity=request.param)
    else:
        raise TypeError(f"What the heck did you request? {request.param}")

    bc.is_lured = True
    return bc


@pytest.fixture
def bc_random_trapped():
    """Return a random, trapped BattleCog with battle_id == 1"""
    bc = BattleCog(battle_id=1, entity=get_random_cog())
    bc.is_trapped = True
    return bc
