import pytest

from ...Battle import AttackProcessor, Battle
from ...Cog import Cog
from ...Factory import BattleCogFactory, CogFactory
from ...Toon import Toon

BATTLE_ID = 1

# Cog-specific global variables
KEY_FLUNKY = 'f'
KEY_YESMAN = 'ym'
KEY_PENCIL = 'p'
NAME_FLUNKY = 'Flunky'
COG_LVL1 = CogFactory().get_cog(key=KEY_FLUNKY)
COG_LVL4 = CogFactory().get_cog(key=KEY_PENCIL, relative_level=2)
COG_LVL7 = CogFactory().get_cog(key=KEY_YESMAN, relative_level=4)
BC_LVL1 = BattleCogFactory().get_battle_cog(battle_id=BATTLE_ID, entity=COG_LVL1)
BC_LVL7 = BattleCogFactory().get_battle_cog(battle_id=BATTLE_ID, entity=COG_LVL7)


class TestBattleAttackProcessor:
    """Verify attack rewards for Toons in a default Battle"""

    @pytest.fixture(params=[COG_LVL1, COG_LVL4, COG_LVL7])
    def battle(self, toon_astro: Toon, request: Cog) -> Battle:
        battle = Battle()
        battle.add_toon(new_toon=toon_astro)
        battle.add_cog(new_cog=request.param)
        return battle
