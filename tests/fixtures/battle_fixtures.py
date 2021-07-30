import pytest

from ...Battle import BattleToon
from ...Cog import Cog, get_random_cog
from ...Factory import BattleCogFactory
from ...Toon import Toon


@pytest.fixture
def bt_astro(toon_astro: Toon):
    bt_astro = BattleToon(battle_id=1, entity=toon_astro)
    return bt_astro


@pytest.fixture
def bt_trapa(toon_trapa: Toon):
    bt_trapa = BattleToon(battle_id=1, entity=toon_trapa)
    return bt_trapa


@pytest.fixture
def bc_random_lured():
    """Return a random, lured BattleCog with battle_id == 1"""
    return BattleCogFactory(battle_id=1, entity=get_random_cog(), lured=True)


@pytest.fixture
def bc_random_trapped():
    """Return a random, trapped BattleCog with battle_id == 1"""
    return BattleCogFactory(battle_id=1, entity=get_random_cog(), trapped=True)


@pytest.fixture
def bc_lured(request):
    """Given a Cog object, or a (key, rel_lvl) tuple, return a lured BattleCog

    Args:
        cog (Cog): Cog object
        key_rel_lvl (Tuple[str, int]): Cog's key and relative_level in a tuple

    Returns:
        BattleCog: A lured BattleCog
    """
    return BattleCogFactory.get_battle_cog(battle_id=1,
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
    return BattleCogFactory.get_battle_cog(battle_id=1,
                                           entity=get_cog_from_request_param(request.param),
                                           trapped=True)


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
