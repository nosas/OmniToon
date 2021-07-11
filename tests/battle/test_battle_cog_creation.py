from ...Battle import BattleCog
from ...Cog import Cog
from ...Entity import BattleEntity, Entity


class TestBattleCog:

    battle_id = 0
    key = 'f'
    name = 'Flunky'

    def test_battle_cog_creation_default_rel_lvl(self):
        hp = 6
        level = 1
        relative_level = 0

        bc = BattleCog(key=self.key, battle_id=self.battle_id)
        assert bc.battle_id == self.battle_id
        assert bc.key == self.key
        assert bc.name == self.name
        assert bc.hp == hp
        assert bc.level == level
        assert bc.relative_level == relative_level
        assert isinstance(bc, BattleCog)
        assert isinstance(bc, Cog)
        assert isinstance(bc, BattleEntity)
        assert isinstance(bc, Entity)

        bc1 = BattleCog(key=self.key, battle_id=self.battle_id + 1)
        assert bc != bc1
        assert bc1.battle_id == bc.battle_id + 1

        bc.is_lured = True
        assert bc.is_lured and not bc1.is_lured

    def test_battle_cog_creation_nondefault_rel_lvl(self):
        key = 'f'
        name = 'Flunky'
        hp = 12
        level = 2
        relative_level = 1

        bc = BattleCog(key=key, relative_level=relative_level, battle_id=self.battle_id)
        assert bc.battle_id == self.battle_id
        assert bc.key == key
        assert bc.name == name
        assert bc.hp == hp
        assert bc.level == level
        assert bc.relative_level == relative_level
        assert isinstance(bc, BattleCog)
        assert isinstance(bc, Cog)
        assert isinstance(bc, BattleEntity)
        assert isinstance(bc, Entity)

        bc1 = BattleCog(key=key, relative_level=relative_level, battle_id=self.battle_id + 1)
        assert bc != bc1
        assert bc1.battle_id == bc.battle_id + 1

        bc.is_lured = True
        assert bc.is_lured and not bc1.is_lured
