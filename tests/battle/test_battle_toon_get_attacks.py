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

    def test_battle_toon_gag_is_possible(self, bt_astro: BattleToon):
        """
        Verify Astro has only 28 possible Gags against a lvl 1 Flunky.
        Gag possibility does NOT take into account the current quantity of the Gag (Gag.count)

        Gag possibility is True if the Gag is unlocked, not a Heal Gag, not a Lure Gag when the
            target is lured, and not a Trap Gag when the target is trapped.
        """
        possible_gags = []
        for gag in bt_astro.entity.gags.unlocked_gags:
            if bt_astro._gag_is_possible(gag=gag, target=BC):
                possible_gags.append(gag)
        assert len(possible_gags) == 28

    def test_battle_toon_gag_is_viable(self, bt_astro: BattleToon):
        """
        Verify Astro has only 5 viable Gags against a lvl 1 Flunky.
        Gag viability does NOT take into account the current quantity of the Gag (Gag.count)

        Gag viability is True if the Gag is possible (see above) and a lower level than the target.
        """
        viable_gags = []
        for gag in bt_astro.entity.gags.unlocked_gags:
            if bt_astro._gag_is_viable(gag=gag, target=BC):
                viable_gags.append(gag)
        assert len(viable_gags) == 5

    def test_battle_toon_possible_attacks(self, bt_astro: BattleToon):
        possible_attacks = bt_astro.get_possible_attacks(target=BC)
        assert possible_attacks != []
        assert len(possible_attacks) == 15

        bt_astro.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 10
        bt_astro.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10

        possible_attacks = bt_astro.get_possible_attacks(target=BC)
        assert len(possible_attacks) == 17

        bt_astro.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 0
        bt_astro.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0

    def test_battle_toon_viable_attacks(self, bt_astro: BattleToon):
        viable_attacks = bt_astro.get_viable_attacks(target=BC)
        assert viable_attacks == []

        bt_astro.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 10
        bt_astro.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10

        viable_attacks = bt_astro.get_viable_attacks(target=BC)
        assert len(viable_attacks) == 2

        bt_astro.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 0
        bt_astro.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0
