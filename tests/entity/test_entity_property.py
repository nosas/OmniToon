from core.Entity import Entity


class TestEntityProperty:

    def test_entity_property_is_defeated(self):

        e = Entity(name="Test", hp=10)
        assert not e.is_defeated

        e.hp = 0
        assert e.is_defeated
