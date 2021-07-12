import pytest

from ...Attack import Attack
from ...AttackGlobals import ATK_TGT_SINGLE
from ...Entity import BattleEntity
from ...Exceptions import InvalidAttackType

BATTLE_ID = 1
NAME = "Test Name"
HP = 100


class TestBattleEntityPropertyAttack:

    atk_name = "Test Attack"
    dmg = 20
    acc = 100
    group = ATK_TGT_SINGLE

    def test_battle_entity_attack_property(self):
        be = BattleEntity(battle_id=BATTLE_ID, name=NAME, hp=HP)
        assert be.attack is None

        atk = Attack(name=self.atk_name, damage=self.dmg, accuracy=self.acc, group=self.group)
        be.attack = atk

        assert isinstance(be.attack, Attack)

    def test_battle_entity_attack_property_fail(self):
        be = BattleEntity(battle_id=BATTLE_ID, name=NAME, hp=HP)
        assert be.attack is None

        with pytest.raises(InvalidAttackType):
            be.attack = self.dmg
            assert not be.attack


class TestBattleEntityPropertyTargets:

    name = "Test Name"
    hp = 100
    battle_id = 1
    dmg = 20

    def test_battle_entity_targets_property(self):
        be = BattleEntity(battle_id=BATTLE_ID, name=NAME, hp=HP)
        assert be.targets is None

        # be1 = BattleEntity(battle_id=BATTLE_ID, name=NAME, hp=HP)
