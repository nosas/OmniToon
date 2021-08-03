from ...AttackGlobals import MULTIPLIER_DEFAULT
from ...Battle import Battle, BattleCog, BattleToon


class TestBattleCreation:

    def test_battle_creation(self, bt_astro: BattleToon, bc_random: BattleCog):
        battle = Battle()
        battle.add_toon(bt_astro)
        assert bt_astro._reward_multiplier == MULTIPLIER_DEFAULT
        print(battle)
