from ...Battle import BattleCog
from ...Cog import Cog
from ...Entity import BattleEntity, Entity
from ...Factory import BattleCogFactory, BattleEntityFactory, CogFactory

BATTLE_ID = 1
KEY = 'f'
NAME = 'Flunky'


class TestBattleCogDefaultCreation:
    cog = Cog(key=KEY)
    bc = BattleCog(battle_id=BATTLE_ID, entity=cog)

    # Expected values
    hp = 6
    level = 1
    relative_level = 0

    def test_battle_cog_battle_id(self):
        assert self.bc.battle_id == BATTLE_ID

    def test_battle_cog_hp(self):
        assert self.bc.hp == self.hp

    def test_battle_cog_name(self):
        assert self.bc.name == NAME

    def test_battle_cog_key(self):
        assert self.bc.entity.key == self.bc.key == KEY

    def test_battle_cog_level(self):
        assert self.bc.entity.level == self.bc.level == self.level

    def test_battle_cog_relative_level(self):
        assert self.bc.entity.relative_level == self.bc.relative_level == self.relative_level

    def test_battle_cog_type(self):
        assert isinstance(self.bc, BattleCog)
        assert isinstance(self.bc, BattleEntity)
        assert isinstance(self.bc.entity, Cog)
        assert isinstance(self.bc.entity, Entity)

    def test_battle_cog_lure(self):
        """Verify BattleCog instances don't share the `is_lured` property"""
        bc1 = BattleCog(battle_id=BATTLE_ID + 1, entity=Cog(key=KEY))
        assert self.bc != bc1
        assert bc1.battle_id == self.bc.battle_id + 1

        self.bc.is_lured = True
        assert self.bc.is_lured and not bc1.is_lured


class TestBattleCogCreation:
    hp = 12
    level = 2
    relative_level = 1

    cog = Cog(key=KEY, relative_level=relative_level)
    bc = BattleCog(battle_id=BATTLE_ID, entity=cog)

    def test_battle_cog_battle_id(self):
        assert self.bc.battle_id == BATTLE_ID

    def test_battle_cog_hp(self):
        assert self.bc.hp == self.hp

    def test_battle_cog_name(self):
        assert self.bc.name == NAME

    def test_battle_cog_key(self):
        assert self.bc.entity.key == self.bc.key == KEY

    def test_battle_cog_level(self):
        assert self.bc.entity.level == self.bc.level == self.level

    def test_battle_cog_relative_level(self):
        assert self.bc.entity.relative_level == self.bc.relative_level == self.relative_level

    def test_battle_cog_type(self):
        assert isinstance(self.bc, BattleCog)
        assert isinstance(self.bc, BattleEntity)
        assert isinstance(self.bc.entity, Cog)
        assert isinstance(self.bc.entity, Entity)


class TestBattleCogFactoryCreation:
    hp = 6
    level = 1
    relative_level = 0

    c_factory = CogFactory()
    be_factory = BattleEntityFactory()  # To create BattleCog/BattleToons
    bc_factory = BattleCogFactory()  # To create Lured/Trapped BattleCogs

    cog = c_factory.get_cog(key=KEY, relative_level=relative_level)
    bc = be_factory.get_battle_entity(battle_id=BATTLE_ID, entity=cog)
    lc = bc_factory.get_battle_cog(battle_id=BATTLE_ID, entity=cog, lured=True)
    tc = bc_factory.get_battle_cog(battle_id=BATTLE_ID, entity=cog, trapped=True)

    def test_battle_cog_battle_id(self):
        assert self.bc.battle_id == BATTLE_ID

    def test_battle_cog_hp(self):
        assert self.bc.hp == self.hp

    def test_battle_cog_name(self):
        assert self.bc.name == NAME

    def test_battle_cog_key(self):
        assert self.bc.entity.key == self.bc.key == KEY

    def test_battle_cog_level(self):
        assert self.bc.entity.level == self.bc.level == self.level

    def test_battle_cog_relative_level(self):
        assert self.bc.entity.relative_level == self.bc.relative_level == self.relative_level

    def test_battle_cog_type(self):
        assert isinstance(self.bc, BattleCog)
        assert isinstance(self.bc, BattleEntity)
        assert isinstance(self.bc.entity, Cog)
        assert isinstance(self.bc.entity, Entity)

    def test_battle_cog_is_not_lured(self):
        assert self.bc.is_lured is False

    def test_battle_cog_is_not_trapped(self):
        assert self.bc.is_trapped is False

    def test_lured_battle_cog_is_lured(self):
        assert self.lc.is_lured is True
        assert self.lc.is_trapped is False

    def test_trapped_battle_cog_is_trapped(self):
        assert self.tc.is_trapped is True
        assert self.tc.is_lured is False
