import pytest

from ...Attack import Attack
from ...AttackGlobals import GROUP
from ...Battle import BattleCog
from ...Cog import get_random_cog
from ...Entity import BattleEntity, Entity
from ...Exceptions import InvalidTargetError, TargetDefeatedError

# Allow pytest to instantiate BattleEntity by "removing" the class's abstract methods
BattleEntity.__abstractmethods__ = None

BATTLE_ID = 1
NAME = "Test Name"
HP = 100
ENTITY = Entity(name=NAME, hp=HP)
BE = BattleEntity(battle_id=BATTLE_ID, entity=ENTITY)


class TestBattleEntityPropertyAttack:

    atk_name = "Test Attack"
    dmg = 20
    acc = 100
    group = GROUP.SINGLE

    def test_battle_entity_attack_property_default(self):
        assert BE.targets is None

    atk = Attack(name=atk_name, damage=dmg, accuracy=acc, group=group)
    BE.attack = atk

    def test_battle_entity_attack_property_type(self):
        assert isinstance(BE.attack, Attack)

    def test_battle_entity_attack_property_name(self):
        assert BE.attack.name == self.atk_name

    def test_battle_entity_attack_property_damage(self):
        assert BE.attack.damage == self.dmg

    def test_battle_entity_attack_property_accuracy(self):
        assert BE.attack.accuracy == self.acc

    def test_battle_entity_attack_property_group(self):
        assert BE.attack.group == GROUP.SINGLE

    def test_battle_entity_attack_property_fail(self):
        with pytest.raises(ValueError):
            BE.attack = self.dmg
            assert not BE.attack


class TestBattleEntityPropertyTargets:

    def test_battle_entity_targets_property_1battlecog_default(self):
        """Verify the default BattleEntity's target is None"""
        assert BE.targets is None

    def test_battle_entity_targets_property_1battlecog_set(self):
        """Verify setting a new value to BattleEntity.targets adds the BattleCog to the list"""
        BE.targets = BattleCog(entity=get_random_cog(), battle_id=BATTLE_ID)
        assert isinstance(BE.targets, list)
        assert len(BE.targets) == 1
        BE._targets = None

    def test_battle_entity_targets_property_max_battlecogs(self):
        """Verify the BattleEntity.target can reach the maximum of 4 targets"""
        assert BE.targets is None

        battle_cog_list = []
        battle_cog_list.append(BattleCog(entity=get_random_cog(), battle_id=BATTLE_ID))
        battle_cog_list.append(BattleCog(entity=get_random_cog(), battle_id=BATTLE_ID + 1))

        BE.targets = battle_cog_list
        assert len(BE.targets) == 2

        battle_cog_list.append(BattleCog(entity=get_random_cog(), battle_id=BATTLE_ID + 2))
        battle_cog_list.append(BattleCog(entity=get_random_cog(), battle_id=BATTLE_ID + 3))

        BE.targets = battle_cog_list
        assert len(BE.targets) == 4
        BE._targets = None

    def test_battle_entity_targets_property_exceed_max_targets_fail(self):
        """Verify the BattleEntity.target raises an Error when exceeding the maximum of 4 targets"""
        assert BE.targets is None

        battle_cog_list = []
        battle_cog_list.append(BattleCog(entity=get_random_cog(), battle_id=BATTLE_ID))
        battle_cog_list.append(BattleCog(entity=get_random_cog(), battle_id=BATTLE_ID + 1))
        battle_cog_list.append(BattleCog(entity=get_random_cog(), battle_id=BATTLE_ID + 2))
        battle_cog_list.append(BattleCog(entity=get_random_cog(), battle_id=BATTLE_ID + 3))

        BE.targets = battle_cog_list
        assert len(BE.targets) == 4

        battle_cog_list.append(BattleCog(entity=get_random_cog(), battle_id=BATTLE_ID + 4))
        with pytest.raises(Exception):
            BE.targets = battle_cog_list
            assert len(BE.targets) == 4
        BE._targets = None

    def test_battle_entity_targets_property_wrong_type_fail(self):
        """Verify BattleEntity.target raises InvalidTargetError when not targeting a BattleEntity"""
        assert BE.targets is None

        with pytest.raises(InvalidTargetError):
            BE.targets = get_random_cog()

        assert BE.targets is None

        with pytest.raises(InvalidTargetError):
            BE.targets = [get_random_cog()]

        assert BE.targets is None

    def test_battle_entity_targets_property_same_type_fail(self):
        """Verify BattleEntity.target raises InvalidTargetError when not targeting a BattleEntity"""
        with pytest.raises(InvalidTargetError):
            BE.targets = BattleEntity(battle_id=BATTLE_ID + 1, entity=ENTITY)

        with pytest.raises(InvalidTargetError):
            BE.targets = BE

        assert BE.targets is None

    def test_battle_entity_targets_property_defeated_fail(self):
        """Verify BattleEntity.target raises TargetDefeatedError when targeting a defeated Entity"""
        bc = BattleCog(entity=get_random_cog(), battle_id=BATTLE_ID)
        bc._get_attacked(amount=bc.hp)

        assert bc.is_defeated

        with pytest.raises(TargetDefeatedError):
            BE.targets = bc

        assert BE.targets is None
