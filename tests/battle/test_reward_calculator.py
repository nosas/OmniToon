import pytest

from ...AttackGlobals import MULTIPLIER
from ...Battle import RewardCalculator

EXPECTED_DEFAULT_FLOOR = MULTIPLIER.FLOOR1
EXPECTED_DEFAULT_INVASION = MULTIPLIER.NO_INVASION
EXPECTED_DEFAULT_MULTIPLIER = 1
EXPECTED_BASE_REWARDS = [1, 2, 3, 4, 5, 6]
BUILDING_MULTIPLIERS = [MULTIPLIER.FLOOR1, MULTIPLIER.FLOOR2, MULTIPLIER.FLOOR3,
                        MULTIPLIER.FLOOR4, MULTIPLIER.FLOOR5]


class TestRewardCalculatorDefault:
    """Test creating RewardCalculator with default building and invasion values"""
    rc = RewardCalculator()

    def test_reward_calculator(self):
        assert self.rc.multiplier_building == EXPECTED_DEFAULT_FLOOR
        assert self.rc.multiplier_invasion == EXPECTED_DEFAULT_INVASION

    def test_get_multiplier(self):
        assert self.rc.get_multiplier() == EXPECTED_DEFAULT_MULTIPLIER

    # @pytest.mark.parametrize()
    # def test_get_base_reward(self, gag_level):
    #     gag = Gag(exp=0, level=gag_level, track=0, count=0)
    #     attack = ToonAttack(gag=gag, target_cog=BattleCog(key='f'))
    #     assert self.rc.get_base_reward(attack=ToonAttack(gag=Gag)) == MULTIPLIER.INVASION


class TestRewardCalculatorInvasion:
    """Test creating RewardCalculator with non-default invasion values"""
    rc_invasion = RewardCalculator(multiplier_invasion=MULTIPLIER.INVASION)

    def test_reward_calculator(self):
        assert self.rc_invasion.multiplier_building == EXPECTED_DEFAULT_FLOOR
        assert self.rc_invasion.multiplier_invasion == MULTIPLIER.INVASION

    def test_get_multiplier(self):
        assert self.rc_invasion.get_multiplier() == MULTIPLIER.INVASION


@pytest.mark.parametrize('building_floor,expected_building_multiplier', [
                         (1, MULTIPLIER.FLOOR1),
                         (2, MULTIPLIER.FLOOR2),
                         (3, MULTIPLIER.FLOOR3),
                         (4, MULTIPLIER.FLOOR4),
                         (5, MULTIPLIER.FLOOR5)])
class TestRewardCalculatorBuilding:
    """Test creating RewardCalculator with non-default building values"""

    def test_reward_calculator(self, building_floor: int, expected_building_multiplier: float):
        rc_building = RewardCalculator(building_floor=building_floor)
        assert rc_building.multiplier_building == expected_building_multiplier

    def test_get_multiplier(self, building_floor: int, expected_building_multiplier: float):
        rc_building = RewardCalculator(building_floor=building_floor)
        assert rc_building.get_multiplier() == expected_building_multiplier


@pytest.mark.parametrize('building_floor,expected_building_multiplier', [
                         (1, MULTIPLIER.FLOOR1),
                         (2, MULTIPLIER.FLOOR2),
                         (3, MULTIPLIER.FLOOR3),
                         (4, MULTIPLIER.FLOOR4),
                         (5, MULTIPLIER.FLOOR5)])
class TestRewardCalculatorBuildingInvasion:
    """Test creating RewardCalculator with non-default building and invasion values"""
    def test_reward_calculator(self, building_floor: int, expected_building_multiplier: float):
        rc_building_invasion = RewardCalculator(building_floor=building_floor,
                                                multiplier_invasion=MULTIPLIER.INVASION)
        assert rc_building_invasion.multiplier_invasion == MULTIPLIER.INVASION
        assert rc_building_invasion.multiplier_building == expected_building_multiplier

    def test_get_multiplier(self, building_floor: int, expected_building_multiplier: float):
        rc_building_invasion = RewardCalculator(building_floor=building_floor,
                                                multiplier_invasion=MULTIPLIER.INVASION)

        expected_multiplier = expected_building_multiplier * MULTIPLIER.INVASION
        assert rc_building_invasion.get_multiplier() == expected_multiplier
