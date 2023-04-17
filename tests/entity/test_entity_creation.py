import pytest

from core.Entity import Entity
from core.Factory import EntityFactory

NAME = "Test"
HP = 10


class TestEntityCreation:
    def test_entity_creation(self):
        e = Entity(name=NAME, hp=HP)
        assert e.name == NAME
        assert e.hp == HP

        e = Entity(name=NAME, hp=str(HP))
        assert e.name == NAME
        assert e.hp == HP

    def test_entity_creation_hp_fail(self):
        with pytest.raises(ValueError):
            Entity(name=NAME, hp=NAME)

    def test_entity_creation_name_fail(self):
        with pytest.raises(ValueError):
            Entity(name=HP, hp=HP)


class TestEntityFactoryCreation:
    factory = EntityFactory()
    e = factory.get_entity(name=NAME, hp=HP)

    def test_entity_creation(self):
        assert self.e.name == NAME
        assert self.e.hp == HP

    def test_entity_creation_string(self):
        e = EntityFactory().get_entity(name=NAME, hp=str(HP))
        assert e.name == NAME
        assert e.hp == HP

    def test_entity_creation_hp_fail(self):
        with pytest.raises(ValueError):
            self.factory.get_entity(name=NAME, hp=NAME)

    def test_entity_creation_name_fail(self):
        with pytest.raises(ValueError):
            self.factory.get_entity(name=HP, hp=HP)
