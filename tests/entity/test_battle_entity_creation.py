import pytest

from ...Entity import BattleEntity, Entity

# Allow pytest to instantiate BattleEntity by "removing" the class's abstract methods
BattleEntity.__abstractmethods__ = None


class TestBattleEntityCreation:

    name = "Test"
    hp = 100
    battle_id = 1
    fail_battle_id = "my_id"
    e = Entity(name=name, hp=hp)
    be = BattleEntity(battle_id=battle_id, entity=e)

    def test_battle_entity_battle_id(self):
        assert self.be.battle_id == self.battle_id

    def test_battle_entity_id_fail(self):
        with pytest.raises(ValueError):
            self.be = BattleEntity(battle_id=self.fail_battle_id, entity=self.e)
            assert not self.be

    def test_battle_entity_type(self):
        assert isinstance(self.be, BattleEntity)
        assert isinstance(self.be.entity, Entity)

    def test_battle_entity_name(self):
        assert self.be.name == self.be.entity.name == self.e.name == self.name

    def test_battle_entity_hp(self):
        assert self.be.hp == self.be.entity.hp == self.e.hp == self.hp

    def test_battle_entity_is_defeated_false(self):
        assert not self.be.is_defeated
        assert self.be.is_defeated == self.be.entity.is_defeated == self.e.is_defeated

    def test_battle_entity_is_defeated_true(self):
        self.be._get_attacked(amount=self.hp)
        assert self.be.is_defeated
        assert self.be.is_defeated == self.be.entity.is_defeated == self.e.is_defeated
