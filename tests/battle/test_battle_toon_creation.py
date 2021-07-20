from ...Battle import BattleToon
from ...Entity import BattleEntity, Entity
from ...Toon import DEFAULT_HP, Inventory, Toon

BATTLE_ID = 1
NAME = 'Mickey'
TOON = Toon(name=NAME)
BT = BattleToon(battle_id=BATTLE_ID, entity=TOON)


class TestBattleToonCreation:

    def test_battle_toon_creation_default_name(self):
        assert BT.name == NAME == BT.entity.name

    def test_battle_toon_creation_default_hp(self):
        BT.hp == DEFAULT_HP

    def test_battle_toon_creation_default_inventory(self):
        BT.hp == Inventory()

    def test_battle_toon_creation_default_battle_id(self):
        assert BT.battle_id == BATTLE_ID

    def test_battle_toon_creation_default_type(self):
        assert isinstance(BT, BattleToon)
        assert isinstance(BT, BattleEntity)
        assert isinstance(BT.entity, Toon)
        assert isinstance(BT.entity, Entity)
