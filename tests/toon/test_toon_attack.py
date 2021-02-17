from ..fixtures.toon_fixtures import toon_astro
from ..fixtures.cog_fixtures import cog_flunky
from ...Gag import Gag
from ...GagGlobals import THROW_TRACK, get_gag_name, get_gag_track_name
import pytest


class TestToonAttackThrow:

    gag_track = THROW_TRACK
    gag_level = 3

    def test_choose_throw_ok(self, toon_astro):
        gag_throw = toon_astro.choose_gag(gag_track=self.gag_track,
                                          gag_level=self.gag_level)
        assert type(gag_throw) == Gag
        # TODO Should move the below tests to `test_gag_creation`
        assert gag_throw.track == self.gag_track
        assert gag_throw.level == self.gag_level
        assert gag_throw.exp == toon_astro.get_gag_exp(gag_throw.track)
        assert gag_throw.name == "Whole Fruit Pie"
        assert gag_throw.name == get_gag_name(gag_throw.track, gag_throw.level)
        assert gag_throw.track_name == "Throw"
        assert gag_throw.track_name == get_gag_track_name(gag_throw.track)
        self.gag = gag_throw

    @pytest.mark.xfail(strict=True)
    def test_choose_throw_fail_quantity(self, toon_astro):
        gag_throw = toon_astro.choose_gag(gag_track=self.gag_track,
                                          gag_level=0)
        # TODO : Create NotEnoughGagsError, and test it here
        assert type(gag_throw) == Gag

    @pytest.mark.skip()
    def test_choose_throw_fail_locked(self, toon_astro):
        # TODO Create test to make sure gag is available (unlocked)
        # TODO : Create LockedGagError, and test it here
        pass

    @pytest.mark.xfail(strict=True)
    def test_attack_target_fail(self, toon_astro):
        gag_throw = toon_astro.choose_gag(gag_track=self.gag_track,
                                          gag_level=self.gag_level)
        try:
            toon_astro.do_attack(target=toon_astro, gag_track=self.gag_track,
                                 gag_level=self.gag_level)
        except AssertionError as e:
            raise e

    def test_gag_quantity_after_attack(self, toon_astro, cog_flunky):
        gag_throw = toon_astro.choose_gag(gag_track=self.gag_track,
                                          gag_level=self.gag_level)
        gag_quantity_before = toon_astro.count_gag(gag_track=gag_throw.track,
                                                   gag_level=gag_throw.level)

        toon_astro.do_attack(cog_flunky, gag_throw.track, gag_throw.level)

        gag_quantity_after = toon_astro.count_gag(gag_track=gag_throw.track,
                                                  gag_level=gag_throw.level)
        assert gag_quantity_after == gag_quantity_before - 1

    @pytest.mark.parametrize('cog_flunky', [0, 1, 2, 3, 4], indirect=True)
    def test_throw_damages_flunky(self, toon_astro, cog_flunky):
        # ! Get viable gags, check if gag is viable
        # ! set a flag is viability doesnt matter
        gag_throw = toon_astro.choose_gag(gag_track=self.gag_track,
                                          gag_level=self.gag_level)

        # TODO : Move the before/after prints to `do_attack`?
        # Printing will likely be done in some Battle function that monitors
        # the state of all Entities in the battle, not in the `do_attack` func
        cog_hp_before = cog_flunky.hp
        num_gags_before = toon_astro.count_gag(gag_throw.track,
                                               gag_throw.level)
        print(f"\nBEFORE= cog_hp {cog_hp_before}, num_gags {num_gags_before}")

        toon_astro.do_attack(target=cog_flunky, gag_track=gag_throw.track,
                             gag_level=gag_throw.level)

        print(f"[!] Toon \"{toon_astro.name}\" used lvl {gag_throw.level} "
              f"{gag_throw.track_name}, {gag_throw.name}, for "
              f"{gag_throw.damage} dmg against lvl {cog_flunky.level} "
              f"{cog_flunky.name}")

        cog_hp_after = cog_flunky.hp
        num_gags_after = toon_astro.count_gag(gag_throw.track, gag_throw.level)
        print(f" AFTER= cog_hp {cog_hp_after}, num_gags {num_gags_after}")
        assert cog_hp_after == cog_hp_before - gag_throw.damage

        # ! Gag EXP should be checked after the Battle, not after each attack
        if cog_hp_after <= 0:
            assert cog_flunky.is_defeated()

    @pytest.mark.parametrize('cog_flunky,is_defeated', [
            (0, True), (1, True), (2, True), (3, False), (4, False)
        ], indirect=["cog_flunky"]
        )
    def test_throw_defeats_flunky(self, toon_astro, cog_flunky, is_defeated):
        gag_throw = toon_astro.choose_gag(gag_track=self.gag_track,
                                          gag_level=self.gag_level)
        cog_hp_before = cog_flunky.hp
        print(f"\nBEFORE= cog_hp {cog_hp_before}")

        toon_astro.do_attack(target=cog_flunky, gag_track=gag_throw.track,
                             gag_level=gag_throw.level)

        print(f"[!] Toon \"{toon_astro.name}\" used lvl {gag_throw.level} "
              f"{gag_throw.track_name}, {gag_throw.name}, for "
              f"{gag_throw.damage} dmg against lvl {cog_flunky.level} "
              f"{cog_flunky.name}")

        cog_hp_after = cog_flunky.hp
        print(f" AFTER= cog_hp {cog_hp_after}")
        assert cog_hp_after == cog_hp_before - gag_throw.damage
        assert cog_flunky.is_defeated() == is_defeated
