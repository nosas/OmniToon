import pytest
from ttr_ai.Toon import (
    Toon, DEFAULT_HP, DEFAULT_LEVELS, DEFAULT_EXPS, DEFAULT_GAGS,
    DEFAULT_GAG_LIMIT
)
from ttr_ai.GagGlobals import (
    GAG_TRACK_LABELS,
    count_all_gags
)


# ? Create file for fixtures? In tests/ directory? Or their respective dirs?
# ? E.g. These toon_X fixtures go in tests/toon/fixtures.py
@pytest.fixture
def toon_astro():
    name = "Astro"
    health = 65
    levels = [5, 0, 6, 5, 5, 5, 2]
    exps = [7421, 0, 10101, 9443, 8690, 6862, 191]
    gags = [[0, 0, 0, 5, 5, 3, 0],  # Toon-up
            [0, 0, 0, 0, 0, 0, 0],  # Trap
            [0, 0, 0, 0, 5, 3, 1],  # Lure
            [0, 0, 0, 0, 5, 3, 0],  # Sound
            [0, 0, 0, 5, 5, 3, 0],  # Throw
            [0, 0, 0, 5, 5, 3, 0],  # Squirt
            [0, 9, 5, 0, 0, 0, 0]]  # Drop
    gag_limit = 70

    return Toon(name=name, health=health, gags=gags, gag_limit=gag_limit,
                gag_levels=levels, gag_exps=exps)


@pytest.fixture
def toon_default():
    return Toon(name="Mickey Mouse")



class TestDefault:
    """Baseline testing for Toon with Default values"""
    # TODO: Add battle scenarios in `test_toon_battle.py`

    def test_health(self, toon_default):
        assert toon_default.health == DEFAULT_HP

    def test_gags(self, toon_default):
        assert toon_default.gags == DEFAULT_GAGS

    def test_gag_exps(self, toon_default):
        assert toon_default.gag_exps == DEFAULT_EXPS

    def test_levels(self, toon_default):
        assert toon_default.gag_levels == DEFAULT_LEVELS

    def test_gag_limit(self, toon_default):
        assert toon_default.gag_limit == DEFAULT_GAG_LIMIT

    def test_has_gags(self, toon_default):
        assert toon_default.has_gags() is False

    def test_gag_count(self, toon_default):
        assert count_all_gags(toon_default.gags) == 0


class TestAstro:
    """Specific testing against my Toon, Astro"""
    # TODO: Add battle scenarios in `test_toon_battle.py`

    def test_health(self, toon_astro):
        assert toon_astro.health == 65

    def test_gag_exps(self, toon_astro):
        assert toon_astro.gag_exps == [7421, 0, 10101, 9443, 8690, 6862, 191]

    def test_levels(self, toon_astro):
        assert toon_astro.gag_levels == [5, 0, 6, 5, 5, 5, 2]

    def test_gag_limit(self, toon_astro):
        assert toon_astro.gag_limit == 70

    def test_has_gags(self, toon_astro):
        assert toon_astro.has_gags() is True
