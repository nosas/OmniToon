import pytest

from src.battle.attack import Attack
from src.battle.attack_globals import GROUP
from src.battle.battle_entity import BattleEntity
from src.core.entity import Entity
from src.core.exceptions import InvalidTargetError, TargetDefeatedError
from src.factories.utils import create_battle_cog, create_random_cog

# Allow pytest to instantiate BattleEntity by "removing" the class's abstract methods
BattleEntity.__abstractmethods__ = None

BATTLE_ID = 1
NAME = "Test Name"
HP = 100
ENTITY = Entity(name=NAME, hp=HP)
BE = BattleEntity(battle_id=BATTLE_ID, entity=ENTITY)


class TestBattleEntity:
    def test_battle_entity_init(self):
        assert BE.battle_id == BATTLE_ID
        assert BE.entity == ENTITY
        assert BE.hp == HP
        assert BE.name == NAME

    def test_battle_entity_init_invalid_entity(self):
        with pytest.raises(ValueError):
            BattleEntity(battle_id=BATTLE_ID, entity="Invalid Entity")

    def test_battle_entity_init_invalid_battle_id(self):
        with pytest.raises(ValueError):
            BattleEntity(battle_id="Invalid Battle ID", entity=ENTITY)

    def test_battle_entity_get_attacked(self):
        damage = 10
        BE._get_attacked(damage)
        assert BE.hp == HP - damage

    def test_battle_entity_get_healed(self):
        heal = 10
        BE._get_healed(heal)
        assert BE.hp == HP - heal + heal

    def test_battle_entity_choose_action(self):
        with pytest.raises(NotImplementedError):
            BE.choose_action([])

    def test_battle_entity_is_defeated(self):
        assert BE.is_defeated is False
        BE._get_attacked(HP)
        assert BE.is_defeated is True
