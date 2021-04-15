import pytest

from ...Battle import Battle
from ...Cog import get_random_cog
from ...Exceptions import TooManyCogsError, TooManyToonsError
from ..fixtures.cog_fixtures import cog_flunky
from ..fixtures.toon_fixtures import (toon_astro, toon_default, toon_newbi,
                                      toon_ostra, toon_sport)


class TestBattleSetup1Toon:

    def test_battle_setup_1toon_1cog(self, toon_astro, cog_flunky):
        print("*********************************")
        print(type(toon_astro), (type(cog_flunky)))
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        # TODO #36, Create __str__ functions for toons/cogs so they display
        # some useful information when printing
        print(first_battle.toons)
        print(first_battle.cogs)
        # ! TODO #37, Create tests for adding toon,cog, calculating rewards
        # ! TODO #43, Create functionality for removing cog/toon if hp <= 0
        # ! TODO #9, Create functionality for removing all gags if toon.hp <= 0
        first_battle.update()
        print(cog_flunky.hp)


class TestBattleSetupMultipleToons:

    @pytest.mark.parametrize('cog_flunky', [4], indirect=True)
    def test_battle_setup_2toons_1cog(self, toon_astro, toon_ostra,
                                      cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_ostra)
        assert len(first_battle.context.toons) == 2

        first_battle.update()
        first_battle.calculate_rewards()

    def test_battle_setup_3toons_1cog(self, toon_astro, toon_ostra,
                                      toon_newbi, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_ostra)
        first_battle.add_toon(toon_newbi)
        assert len(first_battle.context.toons) == 3

        first_battle.update()
        first_battle.calculate_rewards()

    def test_battle_setup_4toons_1cog(self, toon_astro, toon_ostra,
                                      toon_newbi, toon_sport, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_newbi)
        first_battle.add_toon(toon_ostra)
        first_battle.add_toon(toon_sport)
        assert len(first_battle.context.toons) == 4

        first_battle.update()
        first_battle.calculate_rewards()

    def test_battle_setup_5toons_1cog_fail(self, toon_astro, toon_ostra,
                                           toon_newbi, toon_sport,
                                           toon_default, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_newbi)
        first_battle.add_toon(toon_ostra)
        first_battle.add_toon(toon_sport)

        # There can only be a max of 4 Toons battling at once
        with pytest.raises(TooManyToonsError):
            first_battle.add_toon(toon_default)

        assert len(first_battle.context.toons) == 4
        first_battle.update()
        first_battle.calculate_rewards()

        # ! TODO #37, Create tests for adding toon,cog, calculating rewards
        # ! TODO #43, Create functionality for removing cog/toon if hp <= 0
        # ! TODO #9, Create functionality for removing all gags if toon.hp <= 0


class TestBattleSetupMultipleCogs:

    def test_battle_setup_1toon_2cogs(self, toon_astro, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_cog(new_cog=get_random_cog())
        assert len(first_battle.context.cogs) == 2

    def test_battle_setup_1toon_3cogs(self, toon_astro, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_cog(new_cog=get_random_cog())
        first_battle.add_cog(new_cog=get_random_cog())
        assert len(first_battle.context.cogs) == 3

    def test_battle_setup_1toon_4cogs(self, toon_astro, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_cog(new_cog=get_random_cog())
        first_battle.add_cog(new_cog=get_random_cog())
        first_battle.add_cog(new_cog=get_random_cog())
        assert len(first_battle.context.cogs) == 4

    def test_battle_setup_1toon_5cogs_fail(self, toon_astro, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_cog(new_cog=cog_flunky)
        first_battle.add_cog(new_cog=cog_flunky)
        first_battle.add_cog(new_cog=cog_flunky)

        with pytest.raises(TooManyCogsError):
            first_battle.add_cog(new_cog=cog_flunky)
        assert len(first_battle.context.cogs) == 4


class TestBattleSetupMultipleToonsAndCogs:

    def test_battle_setup_1toon_2cogs(self, toon_astro, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_cog(new_cog=get_random_cog())
        assert len(first_battle.context.cogs) == 2

    def test_battle_setup_2toons_3cogs(self, toon_astro, toon_ostra,
                                       cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_ostra)
        assert len(first_battle.context.toons) == 2
        first_battle.add_cog(new_cog=get_random_cog())
        first_battle.add_cog(new_cog=get_random_cog())
        assert len(first_battle.context.cogs) == 3

    def test_battle_setup_3toons_4cogs(self, toon_astro, toon_ostra,
                                       toon_newbi, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_newbi)
        first_battle.add_toon(toon_ostra)
        assert len(first_battle.context.toons) == 3
        first_battle.add_cog(new_cog=get_random_cog())
        first_battle.add_cog(new_cog=get_random_cog())
        first_battle.add_cog(new_cog=get_random_cog())
        assert len(first_battle.context.cogs) == 4

    def test_battle_setup_4toons_5cogs_fail(self, toon_astro, toon_ostra,
                                            toon_newbi, toon_sport,
                                            cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_newbi)
        first_battle.add_toon(toon_ostra)
        first_battle.add_toon(toon_sport)
        first_battle.add_cog(new_cog=cog_flunky)
        first_battle.add_cog(new_cog=cog_flunky)
        first_battle.add_cog(new_cog=cog_flunky)

        with pytest.raises(TooManyCogsError):
            first_battle.add_cog(new_cog=cog_flunky)
        assert len(first_battle.context.toons) == 4
        assert len(first_battle.context.cogs) == 4

    def test_battle_setup_5toons_5cogs_fail(self, toon_astro, toon_ostra,
                                            toon_newbi, toon_sport,
                                            toon_default, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_newbi)
        first_battle.add_toon(toon_ostra)
        first_battle.add_toon(toon_sport)
        # There can only be a max of 4 Toons battling at once
        with pytest.raises(TooManyToonsError):
            first_battle.add_toon(toon_default)
        assert len(first_battle.context.toons) == 4
        first_battle.add_cog(new_cog=cog_flunky)
        first_battle.add_cog(new_cog=cog_flunky)
        first_battle.add_cog(new_cog=cog_flunky)
        # There can only be a max of 4 Cogs battling at once
        with pytest.raises(TooManyCogsError):
            first_battle.add_cog(new_cog=cog_flunky)
        assert len(first_battle.context.cogs) == 4
