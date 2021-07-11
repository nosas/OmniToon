import pytest

from ...Entity import BattleEntity


class TestEntityCreation:

    battle_id = 1
    fail_battle_id = "my_id"

    def test_battle_entity_creation(self):
        be = BattleEntity(battle_id=self.battle_id)
        assert be.battle_id == self.battle_id
        assert isinstance(be, BattleEntity)

    def test_battle_entity_id_fail(self):
        with pytest.raises(TypeError):
            be = BattleEntity(battle_id=self.fail_battle_id)
            assert not be