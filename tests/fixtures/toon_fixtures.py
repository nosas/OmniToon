import pytest

from core.ToonGlobals import ASTRO_HP, ASTRO_NAME, TRAPA_HP, TRAPA_NAME
from Toon import Toon


@pytest.fixture
def toon_astro(inventory_astro):
    astro = Toon(name=ASTRO_NAME, hp=ASTRO_HP, inventory=inventory_astro)
    return astro


@pytest.fixture
def toon_trapa(inventory_trapa):
    trapa = Toon(name=TRAPA_NAME, hp=TRAPA_HP, inventory=inventory_trapa)
    return trapa
