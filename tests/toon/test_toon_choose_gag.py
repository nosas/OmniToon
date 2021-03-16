import pytest

from ...Exceptions import (InvalidToonAttackTarget, LockedGagError,
                           LockedGagTrackError, NotEnoughGagsError)
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
        gag_squirt = toon_astro.choose_gag(gag_track=self.gag_track,
                                           gag_level=self.gag_level)
        assert type(gag_squirt) == Gag
        # TODO Should move the below tests to `test_gag_creation`
        assert gag_squirt.track == self.gag_track
        assert gag_squirt.level == self.gag_level
        assert gag_squirt.exp == toon_astro.get_gag_exp(gag_squirt.track)

        assert gag_squirt.name == "Seltzer Bottle"
        assert gag_squirt.name == get_gag_name(gag_squirt.track,
                                               gag_squirt.level)

        assert gag_squirt.track_name == "Squirt"
        assert gag_squirt.track_name == get_gag_track_name(gag_squirt.track)

    def test_choose_gag_fail_quantity(self, toon_astro):
        """Verify Toon's `choose_gag` raises a NotEnoughGagsError when passing
        in a Gag level with 0 quantity

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
        """
        with pytest.raises(NotEnoughGagsError):
            gag_squirt = toon_astro.choose_gag(gag_track=self.gag_track,
                                               gag_level=0)
            assert not gag_squirt

    def test_choose_gag_fail_locked_gag(self, toon_astro):
        """Verify Toon's `choose_gag` raises LockedGagError when trying to
        retrieve a locked Gag track or Gag level

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
        """
        with pytest.raises(LockedGagError):
            gag_squirt = toon_astro.choose_gag(gag_track=self.gag_track,
                                               gag_level=6)
            assert not gag_squirt

    def test_choose_gag_fail_locked_track(self, toon_astro):
        """Verify Toon's `choose_gag` raises LockedGagError when trying to
        retrieve a locked Gag track or Gag level

        Args:
            toon_astro (Toon): Toon fixture of my TTR character
        """
        # TODO : Create test to make sure gag is available (unlocked)
        # TODO : Check first if Gag track is unlocked, then Gag level
        # TODO : Create LockedGagError, and test it here
        with pytest.raises(LockedGagTrackError):
            gag_trap = toon_astro.choose_gag(gag_track=TRAP_TRACK,
                                             gag_level=0)
            assert not gag_trap
