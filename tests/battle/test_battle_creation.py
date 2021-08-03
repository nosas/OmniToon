import pytest

from ...AttackGlobals import MULTIPLIER, MULTIPLIER_DEFAULT
from ...Battle import Battle, BattleToon


class TestBattleCreation:

    @pytest.fixture
    def battle(self) -> Battle:
        battle = Battle()
        return battle

    def test_battle_creation(self, battle: Battle):
        assert battle.get_multiplier() == MULTIPLIER_DEFAULT

    def test_battle_add_toon(self, battle: Battle, bt_astro: BattleToon):
        assert battle.toons == []
        battle.add_toon(new_toon=bt_astro)
        assert battle.toons == [bt_astro]
        assert bt_astro._reward_multiplier == battle.get_multiplier()

    def test_battle_update_multiplier(self, battle: Battle, bt_astro: BattleToon):
        battle.add_toon(new_toon=bt_astro)
        assert bt_astro._reward_multiplier == battle.get_multiplier()
        assert bt_astro._reward_multiplier == MULTIPLIER_DEFAULT == MULTIPLIER.NO_INVASION

        battle.start_invasion()
        assert bt_astro._reward_multiplier == battle.get_multiplier() == MULTIPLIER.INVASION

        battle.stop_invasion()
        assert bt_astro._reward_multiplier == battle.get_multiplier()
        assert bt_astro._reward_multiplier == MULTIPLIER_DEFAULT == MULTIPLIER.NO_INVASION

    def test_battle_unregister_toon(self, battle: Battle, bt_astro: BattleToon):
        """
        Verify a BattleToon can be removed from the Battle.toons list and no longer receives updates
        """
        battle.add_toon(new_toon=bt_astro)
        battle.unregister(toon=bt_astro)
        assert battle.toons == []

        battle.start_invasion()
        assert bt_astro._reward_multiplier == MULTIPLIER_DEFAULT == MULTIPLIER.NO_INVASION
