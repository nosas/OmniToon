import pytest

from ...Attack import Attack
from ...AttackGlobals import ATK_TGT_SINGLE
from ...Battle import BattleCog
from ...Cog import get_random_cog
from ...Entity import BattleEntity
from ...Exceptions import (InvalidAttackType, InvalidTargetError,
                           TargetDefeatedError)

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
        assert be.attack.name == self.atk_name
        assert be.attack.damage == self.dmg
        assert be.attack.accuracy == self.acc
        assert be.attack.group == ATK_TGT_SINGLE

    def test_battle_entity_attack_property_fail(self):
        be = BattleEntity(battle_id=BATTLE_ID, name=NAME, hp=HP)
        assert be.attack is None

        with pytest.raises(InvalidAttackType):
            be.attack = self.dmg
            assert not be.attack


class TestBattleEntityPropertyTargets:

    name = "Test Name"
    hp = 100
    dmg = 20

    def test_battle_entity_targets_property_1battlecog_no_list(self):
        be = BattleEntity(battle_id=BATTLE_ID, name=NAME, hp=HP)
        assert be.targets is None

        be.targets = BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID)
        assert isinstance(be.targets, list)
        assert len(be.targets) == 1
        # be1 = BattleEntity(battle_id=BATTLE_ID, name=NAME, hp=HP)

    def test_battle_entity_targets_property_max_battlecogs(self):
        be = BattleEntity(battle_id=BATTLE_ID, name=NAME, hp=HP)
        assert be.targets is None

        battle_cog_list = []
        battle_cog_list.append(BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID))
        battle_cog_list.append(BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID+1))

        be.targets = battle_cog_list
        assert len(be.targets) == 2

        battle_cog_list.append(BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID+2))
        battle_cog_list.append(BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID+3))

        be.targets = battle_cog_list
        assert len(be.targets) == 4

    def test_battle_entity_targets_property_exceed_max_targets_fail(self):
        be = BattleEntity(battle_id=BATTLE_ID, name=NAME, hp=HP)
        assert be.targets is None

        battle_cog_list = []
        battle_cog_list.append(BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID))
        battle_cog_list.append(BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID+1))
        battle_cog_list.append(BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID+2))
        battle_cog_list.append(BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID+3))

        be.targets = battle_cog_list
        assert len(be.targets) == 4

        battle_cog_list.append(BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID+4))
        with pytest.raises(Exception):
            be.targets = battle_cog_list
            assert len(be.targets) == 4

    def test_battle_entity_targets_property_wrong_type_fail(self):
        be = BattleEntity(battle_id=BATTLE_ID, name=NAME, hp=HP)
        assert be.targets is None

        with pytest.raises(InvalidTargetError):
            be.targets = get_random_cog()

        assert be.targets is None

        with pytest.raises(InvalidTargetError):
            be.targets = [get_random_cog()]

        assert be.targets is None

    def test_battle_entity_targets_property_same_type_fail(self):
        bc = BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID)

        with pytest.raises(InvalidTargetError):
            bc.targets = BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID+1)

        with pytest.raises(InvalidTargetError):
            bc.targets = bc

        assert bc.targets is None

    def test_battle_entity_targets_property_defeated_fail(self):
        be = BattleEntity(battle_id=BATTLE_ID, name=NAME, hp=HP)
        bc = BattleCog(cog=get_random_cog(), battle_id=BATTLE_ID)
        bc.hp = 0

        assert bc.is_defeated

        with pytest.raises(TargetDefeatedError):
            be.targets = bc

