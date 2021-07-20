from ...Battle import BattleToon
from ...Entity import BattleEntity, Entity
from ...Gag import Gag, get_default_gags
from ...GagGlobals import GAG
from ...Toon import DEFAULT_HP, Inventory, Toon

BATTLE_ID = 1
NAME = 'Mickey'
TOON = Toon(name=NAME)
BT = BattleToon(battle_id=BATTLE_ID, entity=TOON)


class TestBattleToonCreation:

    def test_battle_toon_creation_default_name(self):
        assert BT.name == NAME == BT.entity.name

    def test_battle_toon_creation_default_hp(self):
        assert BT.hp == DEFAULT_HP == BT.entity.hp

    def test_battle_toon_creation_default_inventory(self):
        assert BT.entity.inventory == Inventory()
        assert BT.entity.inventory.has_gags() is False

    def test_battle_toon_creation_default_gags(self):
        assert BT.entity.inventory.gags.gags == get_default_gags()
        assert BT.entity.inventory.gags.available_gags == []
        assert len(BT.entity.inventory.gags.unlocked_gags) == 2
        default_unlocked_gags = [
            Gag(exp=0, level=GAG.CUPCAKE.level, track=GAG.CUPCAKE.track, count=0),
            Gag(exp=0, level=GAG.SQUIRTING_FLOWER.level, track=GAG.SQUIRTING_FLOWER.track, count=0)
        ]
        assert BT.entity.inventory.gags.unlocked_gags == default_unlocked_gags

    def test_battle_toon_creation_default_battle_id(self):
        assert BT.battle_id == BATTLE_ID

    def test_battle_toon_creation_default_type(self):
        assert isinstance(BT, BattleToon)
        assert isinstance(BT, BattleEntity)
        assert isinstance(BT.entity, Toon)
        assert isinstance(BT.entity, Entity)
