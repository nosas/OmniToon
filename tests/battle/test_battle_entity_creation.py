
from ...Entity import BattleEntity


class TestEntityCreation:

    battle_id = 1

    def test_battle_entity_creation(self):
        be = BattleEntity(battle_id=self.battle_id)
        assert be.battle_id == self.battle_id
        assert isinstance(be, BattleEntity)
