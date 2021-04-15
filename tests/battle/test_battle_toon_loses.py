import pytest

from ...Battle import Battle
from ...BattleState import CogAttackState, LoseState
from ...GagGlobals import count_all_gags
from ..fixtures.cog_fixtures import cog_flunky
from ..fixtures.toon_fixtures import toon_astro


def verify_lose_state(won_battle: Battle):
    assert any([type(state) == LoseState for state in
                won_battle.context._completed_states])


class TestBattleToonLoses:

    @pytest.mark.parametrize('cog_flunky', [4], indirect=True)
    def test_battle_toon_loses_1toon_1cog(self, toon_astro, cog_flunky):
        print("*********************************")
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)

        cog_flunky.hp = 1000
        toon_astro.hp -= (toon_astro.hp - 1)

        while first_battle.is_battling:
            first_battle.update()
        verify_lose_state(first_battle)
        first_battle.calculate_rewards()
        # print(f"`test_battle_toon_loses: {first_battle.calculate_rewards()}")
        # ! TODO #37, Create tests for adding toon,cog, calculating rewards
        # ! TODO #43, Create functionality for removing cog/toon if hp <= 0
        # ! TODO #9, Create functionality for removing all gags if toon.hp <= 0
