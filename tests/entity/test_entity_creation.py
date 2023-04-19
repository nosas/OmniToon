import pytest

from src.core.entity import Entity
from src.factories.utils import create_entity

NAME = "Test"
HP = 10


class TestEntityCreation:
    def test_entity_creation(self):
        e = create_entity(name=NAME, hp=HP)
        assert e.name == NAME
        assert e.hp == HP

    def test_entity_creation_string(self):
        e = create_entity(name=NAME, hp=str(HP))
        assert e.name == NAME
        assert e.hp == HP

    def test_entity_creation_hp_fail(self):
        with pytest.raises(ValueError):
            # ValueError: Invalid hp value: Test
            create_entity(name=NAME, hp=NAME)

    def test_entity_creation_name_fail(self):
        with pytest.raises(ValueError):
            # ValueError: Invalid name value: 10
            create_entity(name=HP, hp=HP)
