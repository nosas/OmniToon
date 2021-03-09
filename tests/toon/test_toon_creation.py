from ..fixtures.toon_fixtures import toon_astro, toon_default
from ...Toon import (
    DEFAULT_HP, DEFAULT_LEVELS, DEFAULT_EXPS, DEFAULT_GAGS,
    DEFAULT_GAG_LIMIT
)
from ...GagGlobals import count_all_gags


class TestDefault:
    """Baseline testing for Toon with Default values"""
    # TODO: Add battle scenarios (losing, winning) in `test_toon_battle.py`

    def test_hp(self, toon_default):
        assert toon_default.hp == DEFAULT_HP

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
    # ? Verify structures of the constructor's args, gag[s|[exps|levels|etc.]
    # TODO: Add battle scenarios (losing, winning) in `test_toon_battle.py`
    # ? Are we neglecting any negative tests?
    # ? Yes. But we're only focusing on toon_astro for now, until we can create
    # ? random toons and have multi-toon battle support

    def test_hp(self, toon_astro):
        assert toon_astro.hp == 65

    def test_gag_exps(self, toon_astro):
        assert toon_astro.gag_exps == [7421, 0, 10101, 9443, 8690, 6862, 191]

    def test_levels(self, toon_astro):
        assert toon_astro.gag_levels == [5, -1, 6, 5, 5, 5, 2]

    def test_gag_limit(self, toon_astro):
        assert toon_astro.gag_limit == 70

    def test_has_gags(self, toon_astro):
        assert toon_astro.has_gags() is True
