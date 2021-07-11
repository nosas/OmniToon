
from ...Entity import Entity


class TestEntityCreation:

    def test_entity_creation(self):
        e = Entity(name="Test", hp=10)
        assert e.name == "Test"
        assert e.hp == 10
