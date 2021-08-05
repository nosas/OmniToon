import pytest

from ...AttackGlobals import MULTIPLIER, MULTIPLIER_DEFAULT
from ...Battle import RewardCalculator, ToonAttack
from ...Factory import (BattleCogFactory, CogFactory, GagFactory,
                        ToonAttackFactory)
from ...Gag import TRACK
from ..fixtures.battle_fixtures import (get_expected_reward,
                                        get_reward_calculator)

EXPECTED_DEFAULT_FLOOR = MULTIPLIER.FLOOR1
EXPECTED_DEFAULT_INVASION = MULTIPLIER.NO_INVASION
EXPECTED_DEFAULT_MULTIPLIER = MULTIPLIER_DEFAULT
EXPECTED_BASE_REWARDS = [1, 2, 3, 4, 5, 6]
BUILDING_MULTIPLIERS = [MULTIPLIER.FLOOR1, MULTIPLIER.FLOOR2, MULTIPLIER.FLOOR3,
                        MULTIPLIER.FLOOR4, MULTIPLIER.FLOOR5]

KEY_FLUNKY = 'f'

GAG_FACTORY = GagFactory()
TATK_FACTORY = ToonAttackFactory()
BC_FACTORY = BattleCogFactory()


@pytest.fixture(params=[0, 1, 2, 3, 4, 5, 6], scope='module')
def toon_attack(request) -> ToonAttack:
    """Given a Gag level, return a ToonAttack with target_cog == lvl 1 Flunky"""
    target_cog = CogFactory().get_cog(key=KEY_FLUNKY, relative_level=0)

    return TATK_FACTORY.get_toon_attack(
        gag=GAG_FACTORY.get_gag(track=TRACK.THROW, level=request.param),
        target_cog=BC_FACTORY.get_battle_cog(battle_id=1, entity=target_cog)
        )


class TestRewardCalculatorDefault:
    """Test creating RewardCalculator with default building and invasion values"""
    rc = RewardCalculator()

    def test_reward_calculator_mulitpliers(self):
        assert self.rc.multiplier_building == EXPECTED_DEFAULT_FLOOR
        assert self.rc.multiplier_invasion == EXPECTED_DEFAULT_INVASION

    def test_get_multiplier(self):
        assert self.rc.get_multiplier() == EXPECTED_DEFAULT_MULTIPLIER

    def test_get_base_reward(self, toon_attack: ToonAttack):
        assert self.rc.get_base_reward(attack=toon_attack) == toon_attack.gag.level + 1

    def test_calculate_reward(self, toon_attack: ToonAttack):
        expected_reward = get_expected_reward(toon_attack=toon_attack, rc=self.rc)
        assert self.rc.calculate_reward(attack=toon_attack) == expected_reward


class TestRewardCalculatorInvasion:
    """Test creating RewardCalculator with non-default invasion values"""
    rc = RewardCalculator(is_invasion=True)

    def test_reward_calculator_mulitpliers(self):
        assert self.rc.multiplier_building == EXPECTED_DEFAULT_FLOOR
        assert self.rc.multiplier_invasion == MULTIPLIER.INVASION

    def test_get_multiplier(self):
        assert self.rc.get_multiplier() == MULTIPLIER.INVASION

    def test_get_base_reward(self, toon_attack: ToonAttack):
        assert self.rc.get_base_reward(attack=toon_attack) == toon_attack.gag.level + 1

    def test_calculate_reward(self, toon_attack: ToonAttack):
        expected_reward = get_expected_reward(toon_attack=toon_attack, rc=self.rc)
        assert self.rc.calculate_reward(attack=toon_attack) == expected_reward


class TestRewardCalculatorBuilding:
    """Test creating RewardCalculator with non-default building values"""

    @pytest.fixture(scope='class')
    def rc(self, building_floor: int) -> RewardCalculator:
        return get_reward_calculator(building_floor=building_floor)

    def test_reward_calculator_mulitpliers(self, rc: RewardCalculator, expected_building_multiplier: float):  # noqa
        assert rc.multiplier_building == expected_building_multiplier

    def test_get_multiplier(self, rc: RewardCalculator, expected_building_multiplier: float):
        assert rc.get_multiplier() == expected_building_multiplier

    def test_get_base_reward(self, rc: RewardCalculator, toon_attack: ToonAttack):
        assert rc.get_base_reward(attack=toon_attack) == toon_attack.gag.level + 1

    def test_calculate_reward(self, rc: RewardCalculator, toon_attack: ToonAttack):
        expected_reward = get_expected_reward(toon_attack=toon_attack, rc=rc)
        assert rc.calculate_reward(attack=toon_attack) == expected_reward


class TestRewardCalculatorBuildingInvasion:
    """Test creating RewardCalculator with non-default building and invasion values"""

    @pytest.fixture(scope='class')
    def rc(self, building_floor: int) -> RewardCalculator:
        return get_reward_calculator(building_floor=building_floor, is_invasion=True)

    def test_reward_calculator_mulitpliers(self, rc: RewardCalculator, expected_building_multiplier: float):  # noqa
        assert rc.multiplier_invasion == MULTIPLIER.INVASION
        assert rc.multiplier_building == expected_building_multiplier

    def test_get_multiplier(self, rc: RewardCalculator, expected_building_multiplier: float):
        expected_multiplier = expected_building_multiplier * MULTIPLIER.INVASION
        assert rc.get_multiplier() == expected_multiplier

    def test_get_base_reward(self, rc: RewardCalculator, toon_attack: ToonAttack):
        assert rc.get_base_reward(attack=toon_attack) == toon_attack.gag.level + 1

    def test_calculate_reward(self, rc: RewardCalculator, toon_attack: ToonAttack):
        expected_reward = get_expected_reward(toon_attack=toon_attack, rc=rc)
        assert rc.calculate_reward(attack=toon_attack) == expected_reward
