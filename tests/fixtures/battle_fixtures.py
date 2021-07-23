import pytest

from ...Battle import BattleToon
from ...Toon import Toon


@pytest.fixture
def bt_astro(toon_astro: Toon):
    bt_astro = BattleToon(battle_id=1, entity=toon_astro)
    return bt_astro
