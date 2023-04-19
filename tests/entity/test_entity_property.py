from src.factories.utils import create_entity


class TestEntityProperty:
    def test_entity_property_is_defeated(self):
        e = create_entity(name="Test", hp=10)
        assert not e.is_defeated

        e.hp = 0
        assert e.is_defeated
