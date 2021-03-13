from ..fixtures.toon_fixtures import toon_astro
from ..fixtures.cog_fixtures import cog_flunky
from ...Gag import Gag
from ...GagGlobals import THROW_TRACK, get_gag_name, get_gag_track_name
import pytest


# ? How can we improve Test docstrings? Pass/fail criteria? Raisable errors?
class TestToonAttackThrow:

    gag_track = THROW_TRACK
    gag_level = 3

    def test_choose_throw_ok(self, toon_astro):
        """Verify Toon's `choose_gag` method returns the correct Gag when
        passing in the Gag's track and level as arguments

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
        """
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
        """Verify Toon's `choose_gag` raises a NotEnoughGagsError when passing
        in a Gag level with 0 quantity

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
        """
        gag_throw = toon_astro.choose_gag(gag_track=self.gag_track,
                                          gag_level=0)
        # TODO : Create NotEnoughGagsError, and test it here

    # ! Isn't there a pytest.raises function that catches expected errors?
    @pytest.mark.xfail(strict=True)
    def test_choose_throw_fail_locked(self, toon_astro):
        """Verify Toon's `choose_gag` raises LockedGagError when trying to
        retrieve a locked Gag track or Gag level

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
        """
        # TODO : Create test to make sure gag is available (unlocked)
        # TODO : Check first if Gag track is unlocked, then Gag level
        # TODO : Create LockedGagError, and test it here
        gag_throw = toon_astro.choose_gag(gag_track=self.gag_track,
                                          gag_level=0)
        # TODO : Create NotEnoughGagsError, and test it here

    @pytest.mark.xfail(strict=True)
    def test_attack_target_fail(self, toon_astro):
        """Verify Toon's `do_attack` raises InvalidToonAttackTarget when
        trying to attack a non-Cog object

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
        """
        try:
            toon_astro.do_attack(target=toon_astro, gag_track=self.gag_track,
                                 gag_level=self.gag_level)
        # TODO : Create InvalidTargetError, and test it here
        except AssertionError as e:
            raise e

    def test_gag_quantity_after_attack(self, toon_astro, cog_flunky):
        """Verify quantity of Toon's Gag reduces by 1 after the Toon attacks

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
            cog_flunky (Cog): Flunky Cog fixture
        """
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
        """Verify Toon's attack damages the Cog and reduces the Cog's HP by
        the expected amount.

        This test is repeated against every level of Flunky, from 1-5.

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
            cog_flunky (Cog): Flunky Cog fixture
        """
        # ! Get viable gags, check if gag is viable
        # ! set a flag is viability doesnt matter
        gag_throw = toon_astro.choose_gag(gag_track=self.gag_track,
                                          gag_level=self.gag_level)

        # TODO : Move the before/after prints to `do_attack`?
        # Printing will likely be done in some Battle function that monitors
        # the state of all Entities in the battle, not in the `do_attack` func
        cog_hp_before = cog_flunky.hp
        toon_astro.do_attack(target=cog_flunky, gag_track=gag_throw.track,
                             gag_level=gag_throw.level)

        assert cog_flunky.hp == cog_hp_before - gag_throw.damage

    @pytest.mark.parametrize('cog_flunky,is_defeated', [
            (0, True), (1, True), (2, True), (3, False), (4, False)
        ], indirect=["cog_flunky"]
        )
    def test_throw_defeats_flunky(self, toon_astro, cog_flunky, is_defeated):
        """Verify Toon defeats the Cog if the Gag's damage reduces the
        Cog's HP to <= 0.

        This test is repeated against every level of Flunky, from 1-5.

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
            cog_flunky (Cog): Flunky Cog fixture
        """
        gag_throw = toon_astro.choose_gag(gag_track=self.gag_track,
                                          gag_level=self.gag_level)

        toon_astro.do_attack(target=cog_flunky, gag_track=gag_throw.track,
                             gag_level=gag_throw.level)

        assert cog_flunky.is_defeated() == is_defeated
