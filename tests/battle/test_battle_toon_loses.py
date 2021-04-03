import pytest
from ...BattleState import CogAttackState

from ...Battle import Battle
from ...GagGlobals import count_all_gags
from ..fixtures.cog_fixtures import cog_flunky
from ..fixtures.toon_fixtures import toon_astro


class TestBattleToonLoses:

    @pytest.mark.parametrize('cog_flunky', [4], indirect=True)
    def test_battle_toon_loses_1toon_1cog(self, toon_astro, cog_flunky):
        print("*********************************")
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)

        attack_toon_once = 0
        cog_flunky.hp = 1000

        while first_battle.is_battling:
            while not attack_toon_once:
                # Leave toon_astro with 1hp
                amount = toon_astro.hp - 1
                attack_toon_once = cog_flunky.do_attack(target=toon_astro,
                                                        amount=amount)
            first_battle.update()


        first_battle.calculate_rewards()
        # print(f"`test_battle_toon_loses : {first_battle.calculate_rewards()}")
        # ! TODO #37, Create tests for adding toon,cog, calculating rewards
        # ! TODO #43, Create functionality for removing cog/toon if hp <= 0
        # ! TODO #9, Create functionality for removing all gags if toon.hp <= 0
