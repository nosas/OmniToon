import pytest

from src.core.toon import Inventory
from src.core.toon_globals import ASTRO_GAG_LIMIT, TRAPA_GAG_LIMIT


@pytest.fixture
def inventory_astro(gags_astro):
    inventory_astro = Inventory(gags=gags_astro, max_gags=ASTRO_GAG_LIMIT)
    return inventory_astro


@pytest.fixture
def inventory_trapa(gags_trapa):
    inventory_trapa = Inventory(gags=gags_trapa, max_gags=TRAPA_GAG_LIMIT)
    return inventory_trapa
