import pytest

from ...Gag import Gag
from ...GagGlobals import HEAL_TRACK, LURE_TRACK
from ..fixtures.toon_fixtures import toon_astro
from ..fixtures.cog_fixtures import cog_flunky


# TODO Create method and test for selecting viable targets, given a Gag
class TestToonViableAttacks:

    @pytest.mark.parametrize('cog_flunky', [0, 1, 2, 3, 4],  indirect=True)
    def test_get_viable_attacks(self, toon_astro, cog_flunky):
        toon_gags = toon_astro.gags
        viable_gags = toon_astro.get_viable_attacks(target=cog_flunky)

        for track_idx, (gag_track, vg_track) in enumerate(zip(toon_gags, viable_gags)):  # noqa
            gag_exp = toon_astro.get_gag_exp(track=track_idx)

            if cog_flunky.is_lured and track_idx == LURE_TRACK:  # noqa
                assert vg_track == [-1]*7
                continue
            if track_idx == HEAL_TRACK:
                assert vg_track == [-1]*7
                continue

            for gag_level, (gag_count, vg_count) in enumerate(zip(gag_track, vg_track)):  # noqa
                g = Gag(exp=gag_exp, track=track_idx, level=gag_level,
                        count=gag_count)

                if gag_count in [0, -1]:  # Gag count == 0 or locked -> invalid
                    assert vg_count == -1
                # Gag level must be less than Cog level
                elif gag_level >= cog_flunky.level:
                    assert vg_count == -1, (
                        f"Gag \"{g.name}\", lvl {g.level} {g.track_name}, "
                        "should be unviable because its level is >= Cog's "
                        f"level {cog_flunky.level}"
                    )
                else:
                    assert vg_count == gag_count, (
                        f"Gag \"{g.name}\", lvl {g.level} {g.track_name}, "
                        f"viable count ({vg_count}) does not match "
                        f"expected Gag count of {gag_count} against lvl "
                        f"{cog_flunky.level} Cog"
                    )
