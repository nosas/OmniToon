import pytest

from ...Exceptions import (LockedGagError, LockedGagTrackError,
                           NotEnoughGagsError)
from ...Gag import Gag
from ...GagGlobals import (SQUIRT_TRACK, TRAP_TRACK, get_gag_name,
                           get_gag_track_name)
from ..fixtures.cog_fixtures import cog_flunky
from ..fixtures.toon_fixtures import toon_astro


# ? How can we improve Test docstrings? Pass/fail criteria? Raisable errors?
class TestToonChooseGag:

    gag_track = SQUIRT_TRACK
    gag_level = 3

    def test_choose_gag_ok(self, toon_astro):
        """Verify Toon's `choose_gag` method returns the correct Gag when
        passing in the Gag's track and level as arguments

        Expected Gag = Level 4 Squirt, Seltzer Bottle

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
        """
        gag_squirt = toon_astro.choose_gag(track=self.gag_track,
                                           level=self.gag_level)
        assert type(gag_squirt) == Gag
        # TODO Should move the below tests to `test_gag_creation`
        assert gag_squirt.track == self.gag_track
        assert gag_squirt.level == self.gag_level
        assert gag_squirt.exp == toon_astro.get_gag_exp(track=gag_squirt.track)

        assert gag_squirt.name == "Seltzer Bottle"
        assert gag_squirt.name == get_gag_name(track=gag_squirt.track,
                                               level=gag_squirt.level)

        assert gag_squirt.track_name == "Squirt"
        assert gag_squirt.track_name == get_gag_track_name(
            track=gag_squirt.track)

    # Create negative tests for random gag
    def test_choose_gag_random_ok(self, toon_astro):
        # ! This test hangs..
        for _ in range(25):
            random_gag = toon_astro._pick_random_gag()
            level, name, track = (random_gag.level,
                                  random_gag.name,
                                  random_gag.track)
            # print(f"Randomly selected {track} Gag: Lvl {level} \"{name}\"")
        pass

    def test_choose_gag_fail_quantity(self, toon_astro):
        """Verify Toon's `choose_gag` raises a NotEnoughGagsError when passing
        in a Gag level with 0 quantity

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
        """
        with pytest.raises(NotEnoughGagsError):
            gag_squirt = toon_astro.choose_gag(track=self.gag_track, level=0)
            assert not gag_squirt

    def test_choose_gag_fail_locked_gag(self, toon_astro):
        """Verify Toon's `choose_gag` raises LockedGagError when trying to
        retrieve a locked Gag track or Gag level

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
        """
        with pytest.raises(LockedGagError):
            gag_squirt = toon_astro.choose_gag(track=self.gag_track, level=6)
            assert not gag_squirt

    def test_choose_gag_fail_locked_track(self, toon_astro):
        """Verify Toon's `choose_gag` raises LockedGagError when trying to
        retrieve a locked Gag track or Gag level

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
        """
        with pytest.raises(LockedGagTrackError):
            gag_trap = toon_astro.choose_gag(track=TRAP_TRACK, level=0)
            assert not gag_trap
