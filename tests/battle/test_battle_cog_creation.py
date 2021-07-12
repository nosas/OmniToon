from ...Battle import BattleCog
from ...Cog import Cog
from ...Entity import BattleEntity, Entity

BATTLE_ID = 1
KEY = 'f'
NAME = 'Flunky'


class TestBattleCogCreation:

    def test_battle_cog_creation_default_rel_lvl(self):
        hp = 6
        level = 1
        relative_level = 0

        cog = Cog(key=KEY)
        bc = BattleCog(battle_id=BATTLE_ID, cog=cog)
        assert bc.battle_id == BATTLE_ID
        assert bc.name == NAME
        assert bc.hp == hp
        assert bc.cog.key == KEY
        assert bc.cog.level == level
        assert bc.cog.relative_level == relative_level
        assert isinstance(bc, BattleCog)
        assert isinstance(bc, BattleEntity)
        assert isinstance(bc, Entity)
        assert isinstance(bc.cog, Cog)
        assert isinstance(bc.cog, Entity)

        bc1 = BattleCog(battle_id=BATTLE_ID + 1, cog=Cog(key=KEY))
        assert bc != bc1
        assert bc1.battle_id == bc.battle_id + 1

        bc.is_lured = True
        assert bc.is_lured and not bc1.is_lured

    def test_battle_cog_creation_nondefault_rel_lvl(self):
        hp = 12
        level = 2
        relative_level = 1

        cog = Cog(key=KEY, relative_level=relative_level)
        bc = BattleCog(battle_id=BATTLE_ID, cog=cog)
        assert bc.battle_id == BATTLE_ID
        assert bc.name == NAME
        assert bc.hp == hp
        assert bc.cog.key == KEY
        assert bc.cog.level == level
        assert bc.cog.relative_level == relative_level
        assert isinstance(bc, BattleCog)
        assert isinstance(bc, BattleEntity)
        assert isinstance(bc, Entity)
        assert isinstance(bc.cog, Cog)
        assert isinstance(bc.cog, Entity)

        bc1 = BattleCog(battle_id=BATTLE_ID + 1, cog=Cog(key=KEY, relative_level=relative_level))
        assert bc != bc1
        assert bc1.battle_id == bc.battle_id + 1

        bc.is_lured = True
        assert bc.is_lured and not bc1.is_lured
