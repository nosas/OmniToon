import pytest
from ...Battle import Battle
from ..fixtures.cog_fixtures import cog_flunky
from ..fixtures.toon_fixtures import toon_astro
from ...GagGlobals import count_all_gags


class TestBattleToonWins:

    @pytest.mark.parametrize('cog_flunky', [4], indirect=True)
    def test_battle_toon_wins_1toon_1cog(self, toon_astro, cog_flunky):
        print("*********************************")
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)

        # viable_attacks = toon_astro.get_viable_attacks(target=cog_flunky)
        # while count_all_gags(viable_attacks) != 0:
        while not cog_flunky.is_defeated():
            first_battle.update()
        print(first_battle.calculate_rewards())
        # ! TODO Create tests for adding toon,cog, calculating rewards
        # ! TODO Create functionality for removing cog/toon if their hp <= 0
        # ! TODO Create functionality for removing all gags if toon.hp <= 0
