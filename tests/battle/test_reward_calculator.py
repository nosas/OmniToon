import pytest

from ...AttackGlobals import MULTIPLIER
from ...Battle import RewardCalculator, ToonAttack
from ...Factory import (BattleCogFactory, CogFactory, GagFactory,
                        ToonAttackFactory)
from ...Gag import TRACK

EXPECTED_DEFAULT_FLOOR = MULTIPLIER.FLOOR1
EXPECTED_DEFAULT_INVASION = MULTIPLIER.NO_INVASION
EXPECTED_DEFAULT_MULTIPLIER = 1
EXPECTED_BASE_REWARDS = [1, 2, 3, 4, 5, 6]
BUILDING_MULTIPLIERS = [MULTIPLIER.FLOOR1, MULTIPLIER.FLOOR2, MULTIPLIER.FLOOR3,
                        MULTIPLIER.FLOOR4, MULTIPLIER.FLOOR5]

KEY_FLUNKY = 'f'

GAG_FACTORY = GagFactory()
TATK_FACTORY = ToonAttackFactory()
BC_FACTORY = BattleCogFactory()


@pytest.fixture(params=[0, 1, 2, 3, 4, 5, 6])
def toon_attack(request) -> ToonAttack:
    """Given a Gag level, return a ToonAttack with target_cog == lvl 1 Flunky"""
    target_cog = CogFactory().get_cog(key=KEY_FLUNKY, relative_level=0)

    return TATK_FACTORY.get_toon_attack(
        gag=GAG_FACTORY.get_gag(track=TRACK.THROW, level=request.param),
        target_cog=BC_FACTORY.get_battle_cog(battle_id=1, entity=target_cog)
        )


@pytest.fixture(params=[1, 2, 3, 4, 5])
def building_floor(request):
    """Return all possible building floor values, one at a time"""
    return request.param


@pytest.fixture
def expected_building_multiplier(building_floor) -> float:
    """Given a building_floor value, return the expected building_multiplier value"""
    return MULTIPLIER.get_building_multiplier_from_floor(floor=building_floor)


def get_expected_reward(toon_attack: ToonAttack, rc: RewardCalculator) -> int:
    """Given a ToonAttack and RewardCalculator, return the expected reward value"""
    if toon_attack.gag.level >= toon_attack.target_cog.level:
        return -1
    else:
        return round(rc.get_base_reward(attack=toon_attack) * rc.get_multiplier())


class TestRewardCalculatorDefault:
    """Test creating RewardCalculator with default building and invasion values"""
    rc = RewardCalculator()

    def test_reward_calculator_mulitpliers(self):
        assert self.rc.multiplier_building == EXPECTED_DEFAULT_FLOOR
        assert self.rc.multiplier_invasion == EXPECTED_DEFAULT_INVASION

    def test_get_multiplier(self):
        assert self.rc.get_multiplier() == EXPECTED_DEFAULT_MULTIPLIER

    def test_get_base_reward(self, toon_attack):
        assert self.rc.get_base_reward(attack=toon_attack) == toon_attack.gag.level + 1

    def test_calculate_reward(self, toon_attack):
        expected_reward = get_expected_reward(toon_attack=toon_attack, rc=self.rc)
        assert self.rc.calculate_reward(attack=toon_attack) == expected_reward


class TestRewardCalculatorInvasion:
    """Test creating RewardCalculator with non-default invasion values"""
    rc_invasion = RewardCalculator(multiplier_invasion=MULTIPLIER.INVASION)

    def test_reward_calculator_mulitpliers(self):
        assert self.rc_invasion.multiplier_building == EXPECTED_DEFAULT_FLOOR
        assert self.rc_invasion.multiplier_invasion == MULTIPLIER.INVASION

    def test_get_multiplier(self):
        assert self.rc_invasion.get_multiplier() == MULTIPLIER.INVASION

    def test_get_base_reward(self, toon_attack):
        assert self.rc_invasion.get_base_reward(attack=toon_attack) == toon_attack.gag.level + 1

    def test_calculate_reward(self, toon_attack):
        expected_reward = get_expected_reward(toon_attack=toon_attack, rc=self.rc_invasion)
        assert self.rc_invasion.calculate_reward(attack=toon_attack) == expected_reward


class TestRewardCalculatorBuilding:
    """Test creating RewardCalculator with non-default building values"""

    def test_reward_calculator_mulitpliers(self, building_floor: int, expected_building_multiplier: float):  # noqa
        rc_building = RewardCalculator(building_floor=building_floor)
        assert rc_building.multiplier_building == expected_building_multiplier

    def test_get_multiplier(self, building_floor: int, expected_building_multiplier: float):
        rc_building = RewardCalculator(building_floor=building_floor)
        assert rc_building.get_multiplier() == expected_building_multiplier

    def test_get_base_reward(self, toon_attack, building_floor: int):
        rc_building = RewardCalculator(building_floor=building_floor)
        assert rc_building.get_base_reward(attack=toon_attack) == toon_attack.gag.level + 1

    def test_calculate_reward(self, toon_attack, building_floor: int):
        rc_building = RewardCalculator(building_floor=building_floor)
        expected_reward = get_expected_reward(toon_attack=toon_attack, rc=rc_building)
        assert rc_building.calculate_reward(attack=toon_attack) == expected_reward


class TestRewardCalculatorBuildingInvasion:
    """Test creating RewardCalculator with non-default building and invasion values"""

    def test_reward_calculator_mulitpliers(self, building_floor: int, expected_building_multiplier: float):  # noqa
        rc_building_invasion = RewardCalculator(building_floor=building_floor,
                                                multiplier_invasion=MULTIPLIER.INVASION)
        assert rc_building_invasion.multiplier_invasion == MULTIPLIER.INVASION
        assert rc_building_invasion.multiplier_building == expected_building_multiplier

    def test_get_multiplier(self, building_floor: int, expected_building_multiplier: float):
        rc_building_invasion = RewardCalculator(building_floor=building_floor,
                                                multiplier_invasion=MULTIPLIER.INVASION)

        expected_multiplier = expected_building_multiplier * MULTIPLIER.INVASION
        assert rc_building_invasion.get_multiplier() == expected_multiplier

    def test_get_base_reward(self, toon_attack, building_floor: int):
        rc_building_invasion = RewardCalculator(building_floor=building_floor,
                                                multiplier_invasion=MULTIPLIER.INVASION)
        assert rc_building_invasion.get_base_reward(attack=toon_attack) == toon_attack.gag.level + 1

    def test_calculate_reward(self, toon_attack, building_floor: int):
        rc_building_invasion = RewardCalculator(building_floor=building_floor,
                                                multiplier_invasion=MULTIPLIER.INVASION)
        expected_reward = get_expected_reward(toon_attack=toon_attack, rc=rc_building_invasion)
        assert rc_building_invasion.calculate_reward(attack=toon_attack) == expected_reward
