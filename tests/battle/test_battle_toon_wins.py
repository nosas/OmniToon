import pytest
from ...Battle import Battle
from ..fixtures.cog_fixtures import cog_flunky
from ..fixtures.toon_fixtures import (toon_astro, toon_newbi, toon_ostra,
                                      toon_sport)


class TestBattleToonWins1Cog:

    @pytest.mark.parametrize('cog_flunky', [4], indirect=True)
    def test_battle_toon_wins_1toon_1cog(self, toon_astro, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)

        while first_battle.is_battling:
            first_battle.update()
        first_battle.calculate_rewards()

    @pytest.mark.parametrize('cog_flunky', [4], indirect=True)
    def test_battle_toon_wins_2toons_1cog(self, toon_astro, toon_ostra,
                                          cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_ostra)

        while first_battle.is_battling:
            first_battle.update()
        first_battle.calculate_rewards()

    @pytest.mark.parametrize('cog_flunky', [4], indirect=True)
    def test_battle_toon_wins_3toons_1cog(self, toon_astro, toon_ostra,
                                          toon_newbi, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_ostra)
        first_battle.add_toon(toon_newbi)

        while first_battle.is_battling:
            first_battle.update()
        first_battle.calculate_rewards()

    @pytest.mark.parametrize('cog_flunky', [4], indirect=True)
    def test_battle_toon_wins_4toons_1cog(self, toon_astro, toon_ostra,
                                          toon_newbi, toon_sport, cog_flunky):
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        first_battle.add_toon(toon_newbi)
        first_battle.add_toon(toon_ostra)
        first_battle.add_toon(toon_sport)

        while first_battle.is_battling:
            first_battle.update()
        first_battle.calculate_rewards()

        # ! TODO #37, Create tests for adding toon,cog, calculating rewards
        # ! TODO #43, Create functionality for removing cog/toon if hp <= 0
        # ! TODO #9, Create functionality for removing all gags if toon.hp <= 0


class TestBattleToonWins2Cogs:
