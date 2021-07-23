import pytest

from ...Toon import Inventory
from ...ToonGlobals import ASTRO_GAG_LIMIT


@pytest.fixture
def inventory_astro(gags_astro):
    inventory_astro = Inventory(gags=gags_astro, max_gags=ASTRO_GAG_LIMIT)
    return inventory_astro
