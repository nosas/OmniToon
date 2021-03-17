import pytest

from ...GagGlobals import LURE_TRACK
from ..fixtures.toon_fixtures import toon_astro
from ..fixtures.cog_fixtures import cog_flunky


# TODO Create method and test for selecting viable targets, given a Gag
class TestToonViableAttacks:

    @pytest.mark.parametrize('cog_flunky', [0, 1, 2, 3, 4],  indirect=True)
    def test_get_viable_attacks(self, toon_astro, cog_flunky):
        toon_gags = toon_astro.gags
        viable_gags = toon_astro.get_viable_attacks(target=cog_flunky)

        for gag_track, vg_track in zip(toon_gags, viable_gags):
            if cog_flunky.is_lured and viable_gags.index(vg_track) == LURE_TRACK:  # noqa
                assert viable_gags[vg_track] == [-1]*7

            for gag_level, (gag_count, vg_count) in enumerate(zip(gag_track, vg_track)):  # noqa
                if gag_count in [0, -1]:
                    assert vg_count == -1
                elif gag_level >= cog_flunky.level:
                    assert vg_count == -1
                else:
                    assert vg_count == gag_count

        # TODO Create Rules for valid Gags using numpy masks, validate against
        # those Rules. We can make more custom exceptions for this when we make
        # strategies.

    # TODO Create Toon method to pick random Gag from viable_gags
