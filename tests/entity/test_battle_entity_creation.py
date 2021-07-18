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

    def test_battle_entity_creation(self):

        be = BattleEntity(battle_id=self.battle_id, entity=self.e)
        assert be.battle_id == self.battle_id
        assert isinstance(be, BattleEntity)
        assert isinstance(be.entity, Entity)
        assert be.name == be.entity.name == self.e.name == self.name
        assert be.hp == be.entity.hp == self.e.hp == self.hp
        assert not be.is_defeated
        assert be.is_defeated == be.entity.is_defeated == self.e.is_defeated

        be._get_attacked(amount=self.hp)
        assert be.is_defeated
        assert be.is_defeated == be.entity.is_defeated == self.e.is_defeated

    def test_battle_entity_id_fail(self):
        with pytest.raises(TypeError):
            be = BattleEntity(battle_id=self.fail_battle_id, entity=self.e)
            assert not be
