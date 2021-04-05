import pytest
from ...Battle import Battle
from ..fixtures.cog_fixtures import cog_flunky
from ..fixtures.toon_fixtures import (toon_astro, toon_default, toon_newbi,
                                      toon_ostra, toon_sport)


class TestBattleSetup1Toon:

    def test_battle_1toon_1cog(self, toon_astro, cog_flunky):
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
        print(first_battle.cogs[0].hp)


class TestBattleSetupMultipleToons:

    @pytest.mark.parametrize('cog_flunky', [4], indirect=True)
    def test_battle_toon_wins_2toons_1cog(self, toon_astro, toon_ostra,
                                          cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_ostra)

        first_battle.update()
        first_battle.calculate_rewards()

    def test_battle_toon_wins_3toons_1cog(self, toon_astro, toon_ostra,
                                          toon_newbi, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_ostra)
        first_battle.add_toon(toon_newbi)

        first_battle.update()
        first_battle.calculate_rewards()

    def test_battle_toon_wins_4toons_1cog(self, toon_astro, toon_ostra,
                                          toon_newbi, toon_sport, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_newbi)
        first_battle.add_toon(toon_ostra)
        first_battle.add_toon(toon_sport)

        first_battle.update()
        first_battle.calculate_rewards()

    def test_battle_toon_wins_5toons_1cog_fail(self, toon_astro, toon_ostra,
                                               toon_newbi, toon_sport,
                                               toon_default, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_newbi)
        first_battle.add_toon(toon_ostra)
        first_battle.add_toon(toon_sport)

        # There can only be a max of 4 Toons battling at once
        first_battle.add_toon(toon_default)

        first_battle.update()
        first_battle.calculate_rewards()

        # ! TODO #37, Create tests for adding toon,cog, calculating rewards
        # ! TODO #43, Create functionality for removing cog/toon if hp <= 0
        # ! TODO #9, Create functionality for removing all gags if toon.hp <= 0
