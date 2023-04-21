import pytest

from src.battle.attack_globals import MULTIPLIER, MULTIPLIER_DEFAULT
from src.battle.battle import Battle
from src.core.cog import Cog
from src.core.toon import Toon
from src.factories.utils import create_battle_cog, create_random_cog


class TestBattleCreation:
    @pytest.fixture
    def battle(self) -> Battle:
        battle = Battle()
        return battle

    def test_battle_creation(self, battle: Battle):
        assert battle.cogs == []
        assert battle.toons == []

    def test_battle_add_cog(self, battle: Battle, c_random: Cog = create_random_cog()):
        battle.add_cog(new_cog=c_random)
        assert battle.cogs == [create_battle_cog(battle_id=0, entity=c_random)]

    def test_battle_add_toon(self, battle: Battle, toon_astro: Toon):
        battle.add_toon(new_toon=toon_astro)
        assert battle.toons == [battle.toons[0]]

    def test_battle_remove_battle_toon(self, battle: Battle, toon_astro: Toon):
        """
        Verify a BattleToon can be removed from src.the Battle.toons list and no longer receives updates
        """
        battle.add_toon(new_toon=toon_astro)
        bt_astro = battle.toons[0]

        battle.remove_battle_toon(btoon=bt_astro)
        assert battle.toons == []

    def test_battle_remove_battle_cog(
        self, battle: Battle, c_random: Cog = create_random_cog()
    ):
        battle.add_cog(new_cog=c_random)
        battle.remove_battle_cog(battle.cogs[0])
        assert battle.cogs == []
