from ..fixtures.toon_fixtures import toon_astro
from ..fixtures.cog_fixtures import cog_flunky
from ...GagGlobals import *
from ...GagGlobals import get_gag_damage
import pytest


class TestToonAttack:
    @pytest.mark.parametrize('cog_flunky', ([0, 1, 2, 3, 4]), indirect=True)
    def test_throw_flunky(self, toon_astro, cog_flunky):
        # ! Get viable gags, check if gag is viable
        # ! set a flag is viability doesnt matter
        gag_track = THROW_TRACK
        gag_level = 3
        # assert toon_astro.has_gag(gag_track=gag_track, gag=gag_level)
        gag_exp = toon_astro.gag_exps[gag_track]  # ? Rename this to track_exp?
        gag_damage = get_gag_damage(gag_track=gag_track, gag_level=gag_level,
                                    exp=gag_exp)
        print(gag_damage)
        # import pdb;pdb.set_trace()
        # TODO : Move the before/after prints to `do_attack`?
        cog_hp_before = cog_flunky.hp
        num_gags_before = toon_astro.gags[gag_track][gag_level]
        track_exp_before = toon_astro.gag_exps[gag_track]
        print(cog_hp_before, num_gags_before, track_exp_before)

        toon_astro.do_attack(target=cog_flunky, gag_track=gag_track,
                             gag_level=gag_level)

        gag_track_name = GAG_TRACK_LABELS[gag_track]
        gag_name = GAG_LABELS[gag_track][gag_level-1]
        cog_level = cog_flunky.level
        print(f"[!] Toon \"{toon_astro.name}\" used lvl {gag_level} "\
              f"{gag_track_name}, {gag_name}, against lvl {cog_level} "\
              f"{cog_flunky.name}")

        cog_hp_after = cog_flunky.hp
        num_gags_after = toon_astro.gags[gag_track][gag_level]
        track_exp_after = toon_astro.gag_exps[gag_track]
        print(cog_hp_after, num_gags_after, track_exp_after)

        assert cog_hp_after == cog_hp_before - gag_damage
        assert num_gags_after == num_gags_before - 1
        assert track_exp_after == track_exp_before + gag_level