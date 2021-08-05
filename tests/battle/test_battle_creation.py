import pytest

from ...AttackGlobals import MULTIPLIER, MULTIPLIER_DEFAULT
from ...Battle import Battle, BattleCog, BattleToon
from ...Cog import get_random_cog


class TestBattleCreation:

    @pytest.fixture
    def battle(self) -> Battle:
        battle = Battle()
        return battle

    def test_battle_creation(self, battle: Battle):
        assert battle.get_multiplier() == MULTIPLIER_DEFAULT
        assert battle.cogs == []
        assert battle.toons == []

    def test_battle_add_cog(self, battle: Battle, c_random: BattleCog = get_random_cog()):
        battle.add_cog(new_cog=c_random)
        assert battle.cogs == [BattleCog(battle_id=1, entity=c_random)]

    def test_battle_add_toon(self, battle: Battle, bt_astro: BattleToon):
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

    def test_battle_building_multiplier(self, bt_astro: BattleToon, battle_building: Battle,
                                        expected_building_multiplier: int):
        """Verify a BattleToon receives the building multiplier, even during an invasion"""
        battle_building.add_toon(new_toon=bt_astro)

        assert battle_building.get_multiplier() == expected_building_multiplier
        assert bt_astro._reward_multiplier == battle_building.get_multiplier()

        battle_building.start_invasion()

        assert battle_building.get_multiplier() == expected_building_multiplier * MULTIPLIER.INVASION  # noqa
        assert bt_astro._reward_multiplier == expected_building_multiplier * MULTIPLIER.INVASION

        battle_building.stop_invasion()
        assert battle_building.get_multiplier() == expected_building_multiplier
        assert bt_astro._reward_multiplier == expected_building_multiplier
