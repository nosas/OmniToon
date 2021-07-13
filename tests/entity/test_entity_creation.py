import pytest

from ...Entity import Entity

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
