from ...Battle import BattleCog, BattleToon
from ...Cog import Cog
from ...GagGlobals import GAG, TRACK
from ...Toon import Toon
from ...ToonGlobals import ASTRO_EXPECTED_AVAILABLE_GAGS

BATTLE_ID = 1

# Cog-specific global variables
KEY = 'f'
NAME = 'Flunky'
COG = Cog(key=KEY)
BC = BattleCog(battle_id=BATTLE_ID, entity=COG)
# Toon-specific global variables
NAME = 'Mickey'
TOON = Toon(name=NAME)
BT = BattleToon(battle_id=BATTLE_ID, entity=TOON)


class TestBattleToonDefaultGetAttacks:

    def test_battle_toon_available_gags(self):
        """Verify the default BattleToon has no available Gags"""
        assert BT.available_gags == TOON.gags.available_gags == []

    def test_battle_toon_gag_is_possible(self):
        """Verify the default BattleToon has 2 possible Gags"""
        possible_gags = []
        for gag in BT.entity.gags.unlocked_gags:
            if BT._gag_is_possible(gag=gag, target=BC):
                possible_gags.append(gag)
        assert len(possible_gags) == 2

    def test_battle_toon_gag_is_viable(self):
        """Verify the default BattleToon has 2 viable Gags"""
        viable_gags = []
        for gag in BT.entity.gags.unlocked_gags:
            if BT._gag_is_viable(gag=gag, target=BC):
                viable_gags.append(gag)
        assert len(viable_gags) == 2

    def test_battle_toon_possible_attacks(self):
        """Verify BattleToon has 0 possbile atks, restock Gags, BattleToon has 2 possbile atks"""
        possible_attacks = BT.get_possible_attacks(target=BC)
        assert possible_attacks == []

        BT.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 10
        BT.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10

        possible_attacks = BT.get_possible_attacks(target=BC)
        assert len(possible_attacks) == 2

        BT.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 0
        BT.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0

    def test_battle_toon_viable_attacks(self):
        """Verify BattleToon has 0 viable atks, restock Gags, BattleToon has 2 viable atks"""
        viable_attacks = BT.get_viable_attacks(target=BC)
        assert viable_attacks == []

        BT.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 10
        BT.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10

        viable_attacks = BT.get_viable_attacks(target=BC)
        assert len(viable_attacks) == 2

        BT.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 0
        BT.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0


class TestBattleToonGetAttacks:

    def test_battle_toon_available_gags(self, bt_astro: BattleToon):
        assert len(bt_astro.available_gags) == ASTRO_EXPECTED_AVAILABLE_GAGS

    # def test_battle_toon_gag_is_possible(self, bt_astro: BattleToon):
    #     possible_gags = []
    #     for gag in BT.entity.gags.unlocked_gags:
    #         if BT._gag_is_possible(gag=gag, target=BC):
    #             possible_gags.append(gag)
    #     assert len(possible_gags) == 2

    # def test_battle_toon_gag_is_viable(self, bt_astro: BattleToon):
    #     viable_gags = []
    #     for gag in BT.entity.gags.unlocked_gags:
    #         if BT._gag_is_viable(gag=gag, target=BC):
    #             viable_gags.append(gag)
    #     assert len(viable_gags) == 2

    # def test_battle_toon_possible_attacks(self, bt_astro: BattleToon):
    #     possible_attacks = BT.get_possible_attacks(target=BC)
    #     assert possible_attacks == []

    #     BT.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 10
    #     BT.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10

    #     possible_attacks = BT.get_possible_attacks(target=BC)
    #     assert len(possible_attacks) == 2

    #     BT.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 0
    #     BT.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0

    # def test_battle_toon_viable_attacks(self, bt_astro: BattleToon):
    #     viable_attacks = BT.get_viable_attacks(target=BC)
    #     assert viable_attacks == []

    #     BT.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 10
    #     BT.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10

    #     viable_attacks = BT.get_viable_attacks(target=BC)
    #     assert len(viable_attacks) == 2

    #     BT.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 0
    #     BT.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0
