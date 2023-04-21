import pytest

from src.battle.battle_entity import BattleEntity
from src.core.entity import Entity
from src.factories.utils import create_battle_entity, create_entity

# Allow pytest to instantiate BattleEntity by "removing" the class's abstract methods
BattleEntity.__abstractmethods__ = None

NAME = "Test"
HP = 100
BATTLE_ID = 1
FAIL_BATTLE_ID = "my_id"


class TestBattleEntityCreation:
    e = create_entity(name=NAME, hp=HP)
    be = create_battle_entity(battle_id=BATTLE_ID, entity=e)

    def test_battle_entity_battle_id(self):
        assert self.be.battle_id == BATTLE_ID

    def test_battle_entity_id_fail(self):
        with pytest.raises(ValueError):
            self.be = create_battle_entity(battle_id=FAIL_BATTLE_ID, entity=self.e)
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
        assert self.be.hp != 0
        assert self.be.is_defeated == self.be.entity.is_defeated == self.e.is_defeated

    def test_battle_entity_is_defeated_true(self):
        self.be._get_attacked(amount=HP)
        assert self.be.is_defeated
        assert self.be.hp == 0
        assert self.be.is_defeated == self.be.entity.is_defeated == self.e.is_defeated
