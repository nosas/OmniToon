import pytest

from ...Entity import BattleEntity, Entity
from ...Factory import BattleEntityFactory, EntityFactory

# Allow pytest to instantiate BattleEntity by "removing" the class's abstract methods
BattleEntity.__abstractmethods__ = None

NAME = "Test"
HP = 100
BATTLE_ID = 1
FAIL_BATTLE_ID = "my_id"


class TestBattleEntityCreation:
    e = Entity(name=NAME, hp=HP)
    be = BattleEntity(battle_id=BATTLE_ID, entity=e)

    def test_battle_entity_battle_id(self):
        assert self.be.battle_id == BATTLE_ID

    def test_battle_entity_id_fail(self):
        with pytest.raises(ValueError):
            self.be = BattleEntity(battle_id=FAIL_BATTLE_ID, entity=self.e)
            assert not self.be

    def test_battle_entity_type(self):
        assert isinstance(self.be, BattleEntity)
        assert isinstance(self.be.entity, Entity)

    def test_battle_entity_name(self):
        assert self.be.name == self.be.entity.name == self.e.name == NAME

    def test_battle_entity_hp(self):
        assert self.be.hp == self.be.entity.hp == self.e.hp == HP

    def test_battle_entity_is_defeated_false(self):
        assert not self.be.is_defeated
        assert self.be.is_defeated == self.be.entity.is_defeated == self.e.is_defeated

    def test_battle_entity_is_defeated_true(self):
        self.be._get_attacked(amount=HP)
        assert self.be.is_defeated
        assert self.be.is_defeated == self.be.entity.is_defeated == self.e.is_defeated


class TestBattleEntityFactoryCreation:
    e_factory = EntityFactory()
    be_factory = BattleEntityFactory()

    e = e_factory.get_entity(name=NAME, hp=HP)
    be = be_factory.get_battle_entity(battle_id=BATTLE_ID, entity=e)

    def test_battle_entity_battle_id(self):
        assert self.be.battle_id == BATTLE_ID

    def test_battle_entity_id_fail(self):
        with pytest.raises(ValueError):
            self.be = self.be_factory.get_battle_entity(battle_id=FAIL_BATTLE_ID, entity=self.e)
            assert not self.be

    def test_battle_entity_type(self):
        assert isinstance(self.be, BattleEntity)
        assert isinstance(self.be.entity, Entity)

    def test_battle_entity_name(self):
        assert self.be.name == self.be.entity.name == self.e.name == NAME

    def test_battle_entity_hp(self):
        assert self.be.hp == self.be.entity.hp == self.e.hp == HP

    def test_battle_entity_is_defeated_false(self):
        assert not self.be.is_defeated
        assert self.be.is_defeated == self.be.entity.is_defeated == self.e.is_defeated

    def test_battle_entity_is_defeated_true(self):
        self.be._get_attacked(amount=HP)
        assert self.be.is_defeated
        assert self.be.is_defeated == self.be.entity.is_defeated == self.e.is_defeated
