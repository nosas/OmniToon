
from ...Battle import BattleToon
from ...Entity import BattleEntity, Entity
from ...Gag import Gag, get_default_gags
from ...GagGlobals import GAG
from ...Toon import Inventory, Toon
from ...ToonGlobals import (ASTRO_HP, ASTRO_NAME, DEFAULT_HP, TRAPA_HP,
                            TRAPA_NAME)

BATTLE_ID = 0
NAME = 'Mickey'
TOON = Toon(name=NAME)
BT = BattleToon(battle_id=BATTLE_ID, entity=TOON)


class TestBattleToonDefaultCreation:

    def test_battle_toon_default_name(self):
        assert BT.name == NAME == BT.entity.name

    def test_battle_toon_default_hp(self):
        assert BT.hp == DEFAULT_HP == BT.entity.hp

    def test_battle_toon_default_inventory(self):
        assert BT.entity.inventory == Inventory()
        assert BT.entity.inventory.has_gags() is False

    def test_battle_toon_default_gags(self):
        assert BT.entity.inventory.gags.gags == BT.entity.gags.gags == get_default_gags()
        assert BT.entity.inventory.gags.available_gags == BT.entity.gags.available_gags == []
        assert len(BT.entity.inventory.gags.unlocked_gags) == len(BT.entity.gags.unlocked_gags) == 2
        default_unlocked_gags = [
            Gag(exp=0, level=GAG.CUPCAKE.level, track=GAG.CUPCAKE.track, count=0),
            Gag(exp=0, level=GAG.SQUIRTING_FLOWER.level, track=GAG.SQUIRTING_FLOWER.track, count=0)
        ]
        assert BT.entity.inventory.gags.unlocked_gags == default_unlocked_gags

    def test_battle_toon_default_battle_id(self):
        assert BT.battle_id == BATTLE_ID

    def test_battle_toon_default_type(self):
        assert isinstance(BT, BattleToon)
        assert isinstance(BT, BattleEntity)
        assert isinstance(BT.entity, Toon)
        assert isinstance(BT.entity, Entity)


class TestBattleToonAstroCreation:

    def test_battle_toon_name(self, bt_astro: BattleToon, toon_astro: Toon):
        assert bt_astro.name == ASTRO_NAME == toon_astro.name

    def test_battle_toon_hp(self, bt_astro: BattleToon, toon_astro: Toon):
        assert bt_astro.hp == ASTRO_HP == toon_astro.hp

    def test_battle_toon_entity(self, bt_astro: BattleToon, toon_astro: Toon):
        assert bt_astro.entity == toon_astro

    def test_battle_toon_battle_id(self, bt_astro: BattleToon):
        assert bt_astro.battle_id == BATTLE_ID

    def test_battle_toon_type(self, bt_astro: BattleToon):
        assert isinstance(bt_astro, BattleToon)
        assert isinstance(bt_astro, BattleEntity)
        assert isinstance(bt_astro.entity, Toon)
        assert isinstance(bt_astro.entity, Entity)


class TestBattleToonTrapaCreation:

    def test_battle_toon_name(self, bt_trapa: BattleToon, toon_trapa: Toon):
        assert bt_trapa.name == TRAPA_NAME == toon_trapa.name

    def test_battle_toon_hp(self, bt_trapa: BattleToon, toon_trapa: Toon):
        assert bt_trapa.hp == TRAPA_HP == toon_trapa.hp

    def test_battle_toon_entity(self, bt_trapa: BattleToon, toon_trapa: Toon):
        assert bt_trapa.entity == toon_trapa

    def test_battle_toon_battle_id(self, bt_trapa: BattleToon):
        assert bt_trapa.battle_id == BATTLE_ID

    def test_battle_toon_type(self, bt_trapa: BattleToon):
        assert isinstance(bt_trapa, BattleToon)
        assert isinstance(bt_trapa, BattleEntity)
        assert isinstance(bt_trapa.entity, Toon)
        assert isinstance(bt_trapa.entity, Entity)
