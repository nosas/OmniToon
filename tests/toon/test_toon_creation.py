from src.core.Toon import (DEFAULT_BEAN_COUNT, DEFAULT_BEAN_LIMIT, DEFAULT_HP,
                       Inventory, Toon)
from src.gags.Gag import Gags
from src.gags.GagGlobals import (DEFAULT_GAG_COUNT, DEFAULT_GAG_LIMIT,
                             DEFAULT_TRACK_EXPS_CURRENT, DEFAULT_TRACK_LEVELS)

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


class TestToonDefaultCreation:
    t = Toon(name=DEFAULT_NAME)

    def test_toon_default_creation_name(self):
        assert self.t.name == DEFAULT_NAME

    def test_toon_default_creation_hp(self):
        assert self.t.hp == DEFAULT_HP

    def test_toon_default_creation_inventory(self):
        assert self.t.inventory == Inventory()
        assert self.t.has_gags() is False

    def test_toon_default_creation_gags(self):
        assert self.t.gags == Gags()
        assert self.t.gags.gag_count == DEFAULT_GAG_COUNT
        assert self.t.gags.track_exps == DEFAULT_TRACK_EXPS_CURRENT
        assert self.t.gags.track_levels == DEFAULT_TRACK_LEVELS
        assert self.t.inventory.max_gags == DEFAULT_GAG_LIMIT

    def test_toon_default_creation_jellybeans(self):
        assert self.t.inventory.jellybeans == DEFAULT_BEAN_COUNT
        assert self.t.inventory.max_jellybeans == DEFAULT_BEAN_LIMIT


class TestToonCreation:
    astro_gags = Gags(gag_count=GAG_COUNT, track_exps=TRACK_EXPS)
    astro_inventory = Inventory(gags=astro_gags, max_gags=GAG_LIMIT)
    astro = Toon(name=NAME, hp=HP, inventory=astro_inventory)

    def test_toon_default_creation_name(self, toon_astro: Toon):
        assert self.astro.name == NAME == toon_astro.name

    def test_toon_default_creation_hp(self, toon_astro: Toon):
        assert self.astro.hp == HP == toon_astro.hp

    def test_toon_default_creation_inventory(self, toon_astro: Toon):
        assert self.astro.inventory == toon_astro.inventory
        assert self.astro.has_gags() is True

    def test_toon_default_creation_gags(self, toon_astro: Toon):
        assert self.astro.gags == toon_astro.gags
        assert self.astro.gags.gag_count == GAG_COUNT == toon_astro.gags.gag_count
        assert self.astro.gags.track_exps == TRACK_EXPS == toon_astro.gags.track_exps
        assert self.astro.gags.track_levels == LEVELS == toon_astro.gags.track_levels
        assert self.astro.inventory.max_gags == GAG_LIMIT == toon_astro.inventory.max_gags

    def test_toon_default_creation_jellybeans(self, toon_astro: Toon):
        assert self.astro.inventory.jellybeans == DEFAULT_BEAN_COUNT == toon_astro.inventory.jellybeans  # noqa
        assert self.astro.inventory.max_jellybeans == DEFAULT_BEAN_LIMIT == toon_astro.inventory.max_jellybeans  # noqa
