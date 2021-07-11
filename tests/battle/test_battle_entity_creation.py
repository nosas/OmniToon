
from ...Battle import BattleEntity


class TestEntityCreation:

    name = "Test"
    hp = 10
    battle_id = 1

    def test_entity_creation(self):
        e = BattleEntity(name=self.name, hp=self.hp, battle_id=self.battle_id)
        assert e.name == self.name
        assert e.hp == self.hp
        assert e.battle_id == self.battle_id
