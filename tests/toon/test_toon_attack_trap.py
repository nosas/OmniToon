import pytest

from ...Exceptions import InvalidToonAttackTarget
from ...Gag import Gag
from ...GagGlobals import (LURE_TRACK, TRAP_TRACK, get_gag_name,
                           get_gag_track_name)
from ..fixtures.cog_fixtures import cog_flunky
from ..fixtures.toon_fixtures import toon_ostra


# ? How can we improve Test docstrings? Pass/fail criteria? Raisable errors?
class TestToonAttackTrap:

    lure_track = LURE_TRACK
    lure_level = 6
    trap_track = TRAP_TRACK
    trap_level = 2

    def test_choose_trap_ok(self, toon_ostra):
        """Verify Toon's `choose_gag` method returns the correct Gag when
        passing in the Gag's track and level as arguments

        Args:
            toon_ostra (Toon): Toon fixture of my TTR character, Trap unlocked
        """
        gag_trap = toon_ostra.choose_gag(track=self.trap_track,
                                         level=self.trap_level)
        assert type(gag_trap) == Gag
        # TODO Should move the below tests to `test_gag_creation`
        assert gag_trap.track == self.trap_track
        assert gag_trap.level == self.trap_level
        assert gag_trap.exp == toon_ostra.get_gag_exp(gag_trap.track)
        assert gag_trap.name == "Marbles" == get_gag_name(
            track=gag_trap.track, level=gag_trap.level)
        assert gag_trap.track_name == "Trap" == get_gag_track_name(
            track=gag_trap.track)

    def test_choose_lure_ok(self, toon_ostra):
        """Verify Toon's `choose_gag` method returns the correct Gag when
        passing in the Gag's track and level as arguments

        Args:
            toon_ostra (Toon): Toon fixture of my TTR character, Trap unlocked
        """
        gag_lure = toon_ostra.choose_gag(track=self.lure_track,
                                         level=self.lure_level)
        assert type(gag_lure) == Gag
        # TODO Should move the below tests to `test_gag_creation`
        assert gag_lure.track == self.lure_track
        assert gag_lure.level == self.lure_level
        assert gag_lure.exp == toon_ostra.get_gag_exp(gag_lure.track)
        assert gag_lure.name == "Presentation" == get_gag_name(
            track=gag_lure.track, level=gag_lure.level)
        assert gag_lure.track_name == "Lure" == get_gag_track_name(
            track=gag_lure.track)

    def test_gag_quantity_after_attack(self, toon_ostra, cog_flunky):
        """Verify quantity of Toon's Gag reduces by 1 after the Toon attacks

        Args:
            toon_ostra (Toon): Toon fixture of my TTR character, Trap unlocked
            cog_flunky (Cog): Flunky Cog fixture
        """
        gag_lure = toon_ostra.choose_gag(track=self.lure_track,
                                         level=self.lure_level)
        gag_trap = toon_ostra.choose_gag(track=self.trap_track,
                                         level=self.trap_level)

        # Set up the Trap
        trap_count_before_setup = toon_ostra._count_gag(track=gag_trap.track,
                                                        level=gag_trap.level)
        toon_ostra.do_attack(target=cog_flunky, gag_atk=gag_trap)
        assert cog_flunky.is_trapped is True
        trap_count_after_setup = toon_ostra._count_gag(track=gag_trap.track,
                                                       level=gag_trap.level)
        assert trap_count_after_setup == trap_count_before_setup - 1

        # Use Lure to activate the Trap
        lure_count_before_lure = toon_ostra._count_gag(track=gag_lure.track,
                                                       level=gag_lure.level)
        toon_ostra.do_attack(target=cog_flunky, gag_atk=gag_lure)
        assert cog_flunky.is_lured is True
        assert cog_flunky.is_trapped is True
        trap_count_after_lure = toon_ostra._count_gag(track=gag_trap.track,
                                                      level=gag_trap.level)
        lure_count_after_lure = toon_ostra._count_gag(track=gag_lure.track,
                                                      level=gag_lure.level)
        assert trap_count_after_lure == trap_count_before_setup - 1
        assert lure_count_after_lure == lure_count_before_lure - 1

        # Activate the Trap
        cog_flunky.trap[0].do_attack(target=cog_flunky,
                                     gag_atk=cog_flunky.trap[1])
        assert cog_flunky.is_lured is False
        assert cog_flunky.is_trapped is False
        assert cog_flunky.trap is None
        gag_count_after_activate = toon_ostra._count_gag(track=gag_trap.track,
                                                         level=gag_trap.level)
        assert gag_count_after_activate == trap_count_before_setup - 1

    def test_trap_damages_flunky(self, toon_ostra, cog_flunky):
        """Verify Toon's attack damages the Cog and reduces the Cog's HP by
        the expected amount.

        Args:
            toon_ostra (Toon): Toon fixture of my TTR character, Trap unlocked
            cog_flunky (Cog): Flunky Cog fixture
        """
        # ! Get viable gags, check if gag is viable
        # ! set a flag is viability doesnt matter
        gag_lure = toon_ostra.choose_gag(track=self.lure_track,
                                         level=self.lure_level)
        gag_trap = toon_ostra.choose_gag(track=self.trap_track,
                                         level=self.trap_level)
        cog_hp_before = cog_flunky.hp

        toon_ostra.do_attack(target=cog_flunky, gag_atk=gag_trap)
        assert cog_flunky.is_trapped is True
        assert cog_flunky.trap[0] == toon_ostra
        assert str(cog_flunky.trap[1]) == str(gag_trap)
        assert cog_flunky.hp == cog_hp_before

        toon_ostra.do_attack(target=cog_flunky, gag_atk=gag_lure)
        assert cog_flunky.is_lured is True
        assert cog_flunky.is_trapped is True
        assert cog_flunky.trap[0] == toon_ostra
        assert str(cog_flunky.trap[1]) == str(gag_trap)
        assert cog_flunky.hp == cog_hp_before

        cog_flunky.trap[0].do_attack(target=cog_flunky,
                                     gag_atk=cog_flunky.trap[1])
        assert cog_flunky.is_lured is False
        assert cog_flunky.is_trapped is False
        assert cog_flunky.trap is None

        assert cog_flunky.hp == cog_hp_before - gag_trap.damage

    @pytest.mark.parametrize('cog_flunky,is_defeated', [(0, True), (4, False)],
                             indirect=["cog_flunky"])
    def test_trap_defeats_flunky(self, toon_ostra, cog_flunky, is_defeated):
        """Verify Toon defeats the Cog if the Gag's damage reduces the
        Cog's HP to <= 0.

        This test is repeated against every level of Flunky, from 1-5.

        Args:
            toon_ostra (Toon): Toon fixture of my TTR character, Trap unlocked
            cog_flunky (Cog): Flunky Cog fixture
        """
        gag_lure = toon_ostra.choose_gag(track=self.lure_track,
                                         level=self.lure_level)
        gag_trap = toon_ostra.choose_gag(track=self.trap_track,
                                         level=self.trap_level)
        cog_hp_before = cog_flunky.hp

        toon_ostra.do_attack(target=cog_flunky, gag_atk=gag_trap)
        assert cog_flunky.is_trapped is True
        assert cog_flunky.hp == cog_hp_before

        toon_ostra.do_attack(target=cog_flunky, gag_atk=gag_lure)
        assert cog_flunky.is_lured is True
        assert cog_flunky.is_trapped is True
        assert cog_flunky.hp == cog_hp_before

        cog_flunky.trap[0].do_attack(target=cog_flunky,
                                     gag_atk=cog_flunky.trap[1])
        assert cog_flunky.is_lured is False
        assert cog_flunky.is_trapped is False
        assert cog_flunky.trap is None

        assert cog_flunky.hp == cog_hp_before - gag_trap.damage
        assert cog_flunky.is_defeated == is_defeated

    def test_trap_cancels_on_trapped_flunky(self, toon_ostra, cog_flunky):
        gag_trap = toon_ostra.choose_gag(track=self.trap_track,
                                         level=self.trap_level)
        gag_trao = toon_ostra.choose_gag(track=self.trap_track,
                                         level=self.trap_level - 1)
        cog_hp_before = cog_flunky.hp

        toon_ostra.do_attack(target=cog_flunky, gag_atk=gag_trap)
        assert cog_flunky.is_trapped is True
        assert cog_flunky.trap[0] == toon_ostra
        assert str(cog_flunky.trap[1]) == str(gag_trap)
        assert cog_flunky.hp == cog_hp_before

        toon_ostra.do_attack(target=cog_flunky, gag_atk=gag_trao)
        assert cog_flunky.is_trapped is False
        assert cog_flunky.trap is None
        assert cog_flunky.hp == cog_hp_before
