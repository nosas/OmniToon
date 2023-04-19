import pytest

from src.core.toon import Toon
from src.core.toon_globals import ASTRO_HP, ASTRO_NAME, TRAPA_HP, TRAPA_NAME


@pytest.fixture
def toon_astro(inventory_astro):
    astro = Toon(name=ASTRO_NAME, hp=ASTRO_HP, inventory=inventory_astro)
    return astro


@pytest.fixture
def toon_trapa(inventory_trapa):
    trapa = Toon(name=TRAPA_NAME, hp=TRAPA_HP, inventory=inventory_trapa)
    return trapa
