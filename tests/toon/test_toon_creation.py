from ...Gag import Gags
from ...GagGlobals import DEFAULT_GAG_LIMIT
from ...Toon import (DEFAULT_BEAN_COUNT, DEFAULT_BEAN_LIMIT, DEFAULT_HP,
                     Inventory, Toon)

DEFAULT_NAME = "Mickey"

NAME = "Astro"
HP = 65
LEVELS = [5, -1, 6, 5, 5, 5, 2]
TRACK_EXPS = [7421, 0, 10101, 9443, 8690, 6862, 191]
GAG_COUNT = [[0,   0,  0,  5,  5,  3, -1],  # 0 TOON-UP
             [-1, -1, -1, -1, -1, -1, -1],  # 1 TRAP (LOCKED)
             [0,   0,  0,  0,  5,  3,  1],  # 2 LURE
             [0,   0,  0,  0,  5,  3, -1],  # 3 SOUND
             [0,   2,  1,  4,  4,  2, -1],  # 4 THROW
             [0,   0,  0,  5,  5,  3, -1],  # 5 SQUIRT
             [0,   9,  5, -1, -1, -1, -1]]  # 6 DROP
GAG_LIMIT = 70


class TestToonCreation:

    def test_toon_default_creation(self):
        t = Toon(name=DEFAULT_NAME)

        assert t.name == DEFAULT_NAME
        assert t.hp == DEFAULT_HP
        assert t.inventory == Inventory()
        assert t.inventory.gags == Gags()
        assert t.inventory.max_gags == DEFAULT_GAG_LIMIT
        assert t.inventory.jellybeans == DEFAULT_BEAN_COUNT
        assert t.inventory.max_jellybeans == DEFAULT_BEAN_LIMIT

    def test_toon_astro_creation(self):
        astro_gags = Gags(gag_count=GAG_COUNT, track_exps=TRACK_EXPS)
        astro_inventory = Inventory(gags=astro_gags, max_gags=GAG_LIMIT)
        astro = Toon(name=NAME, hp=HP, inventory=astro_inventory)

        assert astro.name == NAME
        assert astro.hp == HP
