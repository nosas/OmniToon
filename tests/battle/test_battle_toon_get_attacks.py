import pytest

from Battle import Battle, BattleCog, BattleToon, RewardCalculator
from Cog import Cog
from core.Factory import BattleCogFactory, CogFactory
from core.GagGlobals import GAG, TRACK
from tests.fixtures.battle_fixtures import get_expected_reward
from Toon import Toon
from ToonGlobals import (ASTRO_EXPECTED_AVAILABLE_GAGS,
                         ASTRO_EXPECTED_TRACK_LEVELS,
                         ASTRO_EXPECTED_UNLOCKED_GAGS,
                         TRAPA_EXPECTED_AVAILABLE_GAGS,
                         TRAPA_EXPECTED_TRACK_LEVELS,
                         TRAPA_EXPECTED_UNLOCKED_GAGS)

BATTLE_ID = 1

# Cog-specific global variables
KEY_FLUNKY = 'f'
KEY_YESMAN = 'ym'
KEY_PENCIL = 'p'
NAME_FLUNKY = 'Flunky'
COG_LVL1 = CogFactory().get_cog(key=KEY_FLUNKY)
COG_LVL4 = CogFactory().get_cog(key=KEY_PENCIL, relative_level=2)
COG_LVL7 = CogFactory().get_cog(key=KEY_YESMAN, relative_level=4)
BC_LVL1 = BattleCogFactory().get_battle_cog(battle_id=BATTLE_ID, entity=COG_LVL1)
BC_LVL7 = BattleCogFactory().get_battle_cog(battle_id=BATTLE_ID, entity=COG_LVL7)
# Default Toon-specific global variables
NAME_TOON = 'Mickey'
TOON = Toon(name=NAME_TOON)
BT = BattleToon(battle_id=BATTLE_ID, entity=TOON)


class TestBattleToonDefaultGetAttacks:

    def test_battle_toon_available_gags(self):
        """Verify the default BattleToon has no available Gags"""
        assert BT.available_gags == TOON.gags.available_gags == []

    def test_battle_toon_gag_is_possible(self):
        """Verify the default BattleToon has 2 possible Gags"""
        possible_gags = []
        for gag in BT.entity.gags.unlocked_gags:
            if BT._gag_is_possible(gag=gag, target=BC_LVL1):
                possible_gags.append(gag)
        assert len(possible_gags) == 2

    def test_battle_toon_gag_is_viable(self):
        """Verify the default BattleToon has 2 viable Gags"""
        viable_gags = []
        for gag in BT.entity.gags.unlocked_gags:
            if BT._gag_is_viable(gag=gag, target=BC_LVL1):
                viable_gags.append(gag)
        assert len(viable_gags) == 2

    def test_battle_toon_possible_attacks(self):
        """Verify BattleToon has 0 possible atks, restock Gags, BattleToon has 2 possible atks"""
        possible_attacks = BT.get_possible_attacks(target=BC_LVL1)
        assert possible_attacks == []

        BT.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 10
        BT.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10

        possible_attacks = BT.get_possible_attacks(target=BC_LVL1)
        assert len(possible_attacks) == 2
        assert all([
            atk.reward == RewardCalculator().get_base_reward(atk) for atk in possible_attacks
        ])

        BT.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 0
        BT.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0

    def test_battle_toon_viable_attacks(self):
        """Verify BattleToon has 0 viable atks, restock Gags, BattleToon has 2 viable atks"""
        viable_attacks = BT.get_viable_attacks(target=BC_LVL1)
        assert viable_attacks == []

        BT.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 10
        BT.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10

        viable_attacks = BT.get_viable_attacks(target=BC_LVL1)
        assert len(viable_attacks) == 2
        assert all([atk.reward >= 1 for atk in viable_attacks])
        BT.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 0
        BT.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0


class TestBattleToonAstroGetAttacks:

    def test_battle_toon_available_gags(self, bt_astro: BattleToon):
        assert len(bt_astro.available_gags) == ASTRO_EXPECTED_AVAILABLE_GAGS

    def test_battle_toon_gag_is_possible(self, bt_astro: BattleToon):
        """
        Verify Astro has only 28 possible Gags against a lvl 1 Flunky.
            NOTE: #28 b/c `bt_astro` has 34 total Gags, but 6 cannot possible be used against
                  the lvl 1 Flunky (6 Toon-Up Gags are impossible attacks against the Flunky)
        Gag possibility does NOT take into account the current quantity of the Gag (Gag.count)
        Gag possibility is True if the Gag is unlocked, not a Heal Gag, not a Lure Gag when the
            target is lured/trapped, and not a Trap Gag when the target is lured/trapped.

        """
        # expected number is 6 unlocked Heal gags
        num_heal_gags = ASTRO_EXPECTED_TRACK_LEVELS[TRACK.HEAL] + 1
        expected_num_gags = ASTRO_EXPECTED_UNLOCKED_GAGS - num_heal_gags
        assert expected_num_gags == 28

        possible_gags = []
        for gag in bt_astro.entity.gags.unlocked_gags:
            if bt_astro._gag_is_possible(gag=gag, target=BC_LVL1):
                assert gag.track != TRACK.HEAL
                possible_gags.append(gag)
        assert len(possible_gags) == expected_num_gags

    def test_battle_toon_gag_is_viable(self, bt_astro: BattleToon):
        """
        Verify Astro has only 5 viable Gags against a lvl 1 Flunky.
        Gag viability does NOT take into account the current quantity of the Gag (Gag.count)

        Gag viability is True if the Gag is possible (see above) and a lower level than the target.
        """
        viable_gags = []
        for gag in bt_astro.entity.gags.unlocked_gags:
            if bt_astro._gag_is_viable(gag=gag, target=BC_LVL1):
                assert gag.track != TRACK.HEAL
                viable_gags.append(gag)
        assert len(viable_gags) == 5

    def test_battle_toon_possible_attacks(self, bt_astro: BattleToon):
        """
        Verify Astro has only 15 possible Attacks, and none are Heal, against a lvl 1 Flunky.

        Possible attacks only consider if the Gag is unlocked and Gag.count > 0.
        Reward (given when the Gag.level is lower than the Cog), is not considered when
            categorizing possible attacks.
        """
        possible_attacks = bt_astro.get_possible_attacks(target=BC_LVL1)
        assert possible_attacks != []
        assert len(possible_attacks) == 15

        bt_astro.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 10
        bt_astro.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10

        possible_attacks = bt_astro.get_possible_attacks(target=BC_LVL1)
        for attack in possible_attacks:
            assert attack.gag.track != TRACK.HEAL
            assert attack.reward == RewardCalculator().calculate_reward(attack=attack)
        assert len(possible_attacks) == 17

        bt_astro.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 0
        bt_astro.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0

    def test_battle_toon_viable_attacks(self, bt_astro: BattleToon):
        """
        Verify Astro has no viable Attacks, and none are Heal, against a lvl 1 Flunky.

        Viable attacks only consider Gags which provide a reward.
            Reward is given when the Gag.level is lower than the Cog.
        """
        viable_attacks = bt_astro.get_viable_attacks(target=BC_LVL1)
        assert viable_attacks == []

        bt_astro.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 10
        bt_astro.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10

        viable_attacks = bt_astro.get_viable_attacks(target=BC_LVL1)
        for attack in viable_attacks:
            assert attack.gag.track != TRACK.HEAL
            assert attack.reward == RewardCalculator().calculate_reward(attack=attack)
            assert attack.reward >= 1
        assert len(viable_attacks) == 2

        bt_astro.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 0
        bt_astro.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0


class TestBattleToonTrapaGetAttacks:
    # expected number is 6 unlocked Heal gags
    num_heal_gags = TRAPA_EXPECTED_TRACK_LEVELS[TRACK.HEAL] + 1

    def test_battle_toon_available_gags(self, bt_trapa: BattleToon):
        assert len(bt_trapa.available_gags) == TRAPA_EXPECTED_AVAILABLE_GAGS

    def test_battle_toon_gag_is_possible(self, bt_trapa: BattleToon):
        """
        Verify Trapa has only 28 possible Gags against a lvl 1 Flunky.
            NOTE: #28 b/c `bt_trapa` has 34 total Gags, but 6 cannot possible be used against
                  the lvl 1 Flunky (6 Toon-Up Gags are impossible attacks against the Flunky)
        Gag possibility does NOT take into account the current quantity of the Gag (Gag.count)
        Gag possibility is True if the Gag is unlocked, not a Heal Gag, not a Lure Gag when the
            target is lured/trapped, and not a Trap Gag when the target is lured/trapped.

        """
        num_heal_gags = TRAPA_EXPECTED_TRACK_LEVELS[TRACK.HEAL] + 1
        expected_num_gags = TRAPA_EXPECTED_UNLOCKED_GAGS - num_heal_gags
        assert expected_num_gags == 28

        possible_gags = []
        for gag in bt_trapa.entity.gags.unlocked_gags:
            if bt_trapa._gag_is_possible(gag=gag, target=BC_LVL1):
                assert gag.track != TRACK.HEAL
                possible_gags.append(gag)
        assert len(possible_gags) == expected_num_gags

    def test_battle_toon_gag_is_viable(self, bt_trapa: BattleToon):
        """
        Verify Trapa has only 5 viable Gags against a lvl 1 Flunky.
        Gag viability does NOT take into account the current quantity of the Gag (Gag.count)

        Gag viability is True if the Gag is possible (see above) and a lower level than the target.
        """
        viable_gags = []
        for gag in bt_trapa.entity.gags.unlocked_gags:
            if bt_trapa._gag_is_viable(gag=gag, target=BC_LVL1):
                assert gag.track != TRACK.HEAL
                viable_gags.append(gag)
        assert len(viable_gags) == 5

    def test_battle_toon_possible_attacks(self, bt_trapa: BattleToon):
        """
        Verify Trapa has only 18 possible Attacks, and none are Heal, against a lvl 1 Flunky.

        Possible attacks only consider if the Gag is unlocked and Gag.count > 0.
        Reward (given when the Gag.level is lower than the Cog), is not considered when
            categorizing possible attacks.
        """
        possible_attacks = bt_trapa.get_possible_attacks(target=BC_LVL1)
        assert possible_attacks != []
        assert len(possible_attacks) == 18

        bt_trapa.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10

        possible_attacks = bt_trapa.get_possible_attacks(target=BC_LVL1)
        for attack in possible_attacks:
            assert attack.gag.track != TRACK.HEAL
        assert len(possible_attacks) == 19

        bt_trapa.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0

    def test_battle_toon_viable_attacks(self, bt_trapa: BattleToon):
        """
        Verify Trapa has 3 viable Attacks, and none are Heal, against a lvl 1 Flunky.

        Viable attacks only consider Gags which provide a reward.
            Reward is given when the Gag.level is lower than the Cog.
        """
        viable_attacks = bt_trapa.get_viable_attacks(target=BC_LVL1)
        assert len(viable_attacks) == 3

        bt_trapa.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10

        viable_attacks = bt_trapa.get_viable_attacks(target=BC_LVL1)
        for attack in viable_attacks:
            assert attack.gag.track != TRACK.HEAL
        assert len(viable_attacks) == 4

        bt_trapa.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0


class TestBattleToonAstroGetAttacksLuredBattleCog:

    @pytest.mark.parametrize('bc_lured', [COG_LVL1], indirect=['bc_lured'])
    def test_battle_toon_gag_is_possible(self, bt_astro: BattleToon, bc_lured: BattleCog):
        """
        Verify Astro has only 21 possible Gags against a lured lvl 1 Flunky.
            NOTE: #28 b/c `bt_astro` has 34 total Gags, but 13 cannot possibly be used against
                  the lured lvl 1 Flunky:
                    - 6 Toon-Up Gags are impossible attacks against the Flunky
                    - 7 Lure Gags are impossible attacks against the lured Flunky
                    - 0 Trap Gags are impossible attacks against the lured Flunky
        Gag possibility does NOT take into account the current quantity of the Gag (Gag.count)
        Gag possibility is True if the Gag is unlocked, not a Heal Gag, not a Lure Gag when the
            target is lured/trapped, and not a Trap Gag when the target is lured/trapped.
        """
        # expected number is 6 unlocked Heal gags
        num_heal_gags = ASTRO_EXPECTED_TRACK_LEVELS[TRACK.HEAL] + 1
        # expected number is 7 unlocked Lure gags
        num_lure_gags = ASTRO_EXPECTED_TRACK_LEVELS[TRACK.LURE] + 1
        # expected number is 0 unlocked Trap gags
        num_trap_gags = ASTRO_EXPECTED_TRACK_LEVELS[TRACK.TRAP] + 1
        sum_num_gags = num_heal_gags + num_lure_gags + num_trap_gags

        expected_num_gags = ASTRO_EXPECTED_UNLOCKED_GAGS - sum_num_gags
        assert expected_num_gags == 21

        possible_gags = []
        for gag in bt_astro.entity.gags.unlocked_gags:
            if bt_astro._gag_is_possible(gag=gag, target=bc_lured):
                assert gag.track not in [TRACK.HEAL, TRACK.LURE, TRACK.TRAP]
                possible_gags.append(gag)
        assert len(possible_gags) == expected_num_gags

    @pytest.mark.parametrize('bc_lured', [COG_LVL1], indirect=['bc_lured'])
    def test_battle_toon_gag_is_viable(self, bt_astro: BattleToon, bc_lured: BattleCog):
        """
        Verify Astro has only 4 viable Gags, and none are Heal/Lure/Trap, against a lured Flunky.
            NOTE: #4 because `bt_astro` has 6 lvl 1 Gags, but 2 cannot possibly be used against
                  the lvl 1 Flunky:
                    - 1 Toon-Up Gag (lvl 0 Toon-Up) is an impossible attack against the Flunky
                    - 1 Lure Gag (lvl 0 Lure) is an impossible attack against the lured Flunky
        Gag viability does NOT take into account the current quantity of the Gag (Gag.count)

        Gag viability is True if the Gag is possible (see above) and a lower level than the target.
        """
        viable_gags = []
        for gag in bt_astro.entity.gags.unlocked_gags:
            if bt_astro._gag_is_viable(gag=gag, target=bc_lured):
                assert gag.track not in [TRACK.HEAL, TRACK.LURE, TRACK.TRAP]
                viable_gags.append(gag)
        assert len(viable_gags) == 4

    @pytest.mark.parametrize('bc_lured', [COG_LVL1], indirect=['bc_lured'])
    def test_battle_toon_possible_attacks(self, bt_astro: BattleToon, bc_lured: BattleCog):
        """
        Verify Astro has only 12 possible Attacks, and none are Heal/Lure, against a lured Flunky.

        Possible attacks only consider if the Gag is unlocked and Gag.count > 0.
        Reward (given when the Gag.level is lower than the Cog), is not considered when
            categorizing possible attacks.
        """
        possible_attacks = bt_astro.get_possible_attacks(target=bc_lured)
        assert possible_attacks != []
        assert len(possible_attacks) == 12

        bt_astro.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 10
        bt_astro.entity.gags.gag_count[TRACK.LURE][GAG.ONE_BILL.level] = 10

        possible_attacks = bt_astro.get_possible_attacks(target=bc_lured)
        assert all([
            atk.gag.track not in [TRACK.HEAL, TRACK.LURE, TRACK.TRAP]
            for atk in possible_attacks
        ])
        assert len(possible_attacks) == 13

        bt_astro.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 0
        bt_astro.entity.gags.gag_count[TRACK.LURE][GAG.ONE_BILL.level] = 0

    @pytest.mark.parametrize('bc_lured', [COG_LVL1], indirect=['bc_lured'])
    def test_battle_toon_viable_attacks(self, bt_astro: BattleToon, bc_lured: BattleCog):
        """
        Verify Astro has no viable Attacks, and none are Heal/Lure, against a lured Flunky.

        Viable attacks only consider Gags which provide a reward.
            Reward is given when the Gag.level is lower than the Cog.
        """
        viable_attacks = bt_astro.get_viable_attacks(target=bc_lured)
        assert viable_attacks == []

        bt_astro.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 10
        bt_astro.entity.gags.gag_count[TRACK.LURE][GAG.ONE_BILL.level] = 10

        viable_attacks = bt_astro.get_viable_attacks(target=bc_lured)
        assert viable_attacks[0].name == GAG.CUPCAKE.name
        assert viable_attacks[0].gag.track == TRACK.THROW
        assert all([atk.gag.track not in [TRACK.HEAL, TRACK.LURE] for atk in viable_attacks])
        assert len(viable_attacks) == 1

        bt_astro.entity.gags.gag_count[TRACK.THROW][GAG.CUPCAKE.level] = 0
        bt_astro.entity.gags.gag_count[TRACK.LURE][GAG.ONE_BILL.level] = 0


class TestBattleToonTrapaGetAttacksLuredBattleCog:

    @pytest.mark.parametrize('bc_lured', [COG_LVL1], indirect=['bc_lured'])
    def test_battle_toon_gag_is_possible(self, bt_trapa: BattleToon, bc_lured: BattleCog):
        """
        Verify Trapa has only 18 possible Gags against a lured lvl 1 Flunky.
            NOTE: #18 b/c `bt_trapa` has 34 total Gags, but 16 cannot possibly be used against
                  the lured lvl 1 Flunky:
                    - 6 Toon-Up Gags are impossible attacks against the Flunky
                    - 7 Lure Gags are impossible attacks against the lured Flunky
                    - 3 Trap Gags are impossible attacks against the lured Flunky
        Gag possibility does NOT take into account the current quantity of the Gag (Gag.count)
        Gag possibility is True if the Gag is unlocked, not a Heal Gag, not a Lure Gag when the
            target is lured/trapped, and not a Trap Gag when the target is lured/trapped.
        """
        # expected number is 6 unlocked Heal gags
        num_heal_gags = TRAPA_EXPECTED_TRACK_LEVELS[TRACK.HEAL] + 1
        # expected number is 7 unlocked Lure gags
        num_lure_gags = TRAPA_EXPECTED_TRACK_LEVELS[TRACK.LURE] + 1
        # expected number is 3 unlocked Trap gags
        num_trap_gags = TRAPA_EXPECTED_TRACK_LEVELS[TRACK.TRAP] + 1
        sum_num_gags = num_heal_gags + num_lure_gags + num_trap_gags

        expected_num_gags = TRAPA_EXPECTED_UNLOCKED_GAGS - sum_num_gags
        assert expected_num_gags == 18

        possible_gags = []
        for gag in bt_trapa.entity.gags.unlocked_gags:
            if bt_trapa._gag_is_possible(gag=gag, target=bc_lured):
                assert gag.track not in [TRACK.HEAL, TRACK.LURE, TRACK.TRAP]
                possible_gags.append(gag)
        assert len(possible_gags) == expected_num_gags

    @pytest.mark.parametrize('bc_lured', [COG_LVL1], indirect=['bc_lured'])
    def test_battle_toon_gag_is_viable(self, bt_trapa: BattleToon, bc_lured: BattleCog):
        """
        Verify Trapa has only 3 viable Gags, and none are Heal/Lure/Trap, against a lured Flunky.
            NOTE: #3 because `bt_trapa` has 6 unlocked lvl 1 Gags, but 3 cannot possibly be used
                  against the lvl 1 Flunky:
                    - 1 Toon-Up Gag (lvl 0 Toon-Up) is an impossible attack against the Flunky
                    - 1 Lure Gag (lvl 0 Lure) is an impossible attack against the lured Flunky
                    - 1 Trap Gag (lvl 0 Trap) is an impossible attack against the lured Flunky
        Gag viability does NOT take into account the current quantity of the Gag (Gag.count)

        Gag viability is True if the Gag is possible (see above) and a lower level than the target.
        """
        viable_gags = []
        for gag in bt_trapa.entity.gags.unlocked_gags:
            if bt_trapa._gag_is_viable(gag=gag, target=bc_lured):
                assert gag.track not in [TRACK.HEAL, TRACK.LURE, TRACK.TRAP]
                viable_gags.append(gag)

        assert len(viable_gags) == 3
        assert viable_gags[0].name == GAG.BIKE_HORN.name
        assert viable_gags[1].name == GAG.CUPCAKE.name
        assert viable_gags[2].name == GAG.SQUIRTING_FLOWER.name

    @pytest.mark.parametrize('bc_lured', [COG_LVL1], indirect=['bc_lured'])
    def test_battle_toon_possible_attacks(self, bt_trapa: BattleToon, bc_lured: BattleCog):
        """
        Verify Trapa has 11 possible Attacks, and none are Heal/Lure/Trap, against a lured Flunky.

        Possible attacks only consider if the Gag is unlocked and Gag.count > 0.
        Reward (given when the Gag.level is lower than the Cog), is not considered when
            categorizing possible attacks.
        """
        possible_attacks = bt_trapa.get_possible_attacks(target=bc_lured)
        assert possible_attacks != []
        assert len(possible_attacks) == 11

        bt_trapa.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10
        bt_trapa.entity.gags.gag_count[TRACK.LURE][GAG.SMALL_MAGNET.level] = 10
        bt_trapa.entity.gags.gag_count[TRACK.HEAL][GAG.FEATHER.level] = 10

        possible_attacks = bt_trapa.get_possible_attacks(target=bc_lured)
        assert all([
            atk.gag.track not in [TRACK.HEAL, TRACK.LURE, TRACK.TRAP]
            for atk in possible_attacks
        ])
        assert len(possible_attacks) == 12

        bt_trapa.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0
        bt_trapa.entity.gags.gag_count[TRACK.LURE][GAG.SMALL_MAGNET.level] = 0
        bt_trapa.entity.gags.gag_count[TRACK.HEAL][GAG.FEATHER.level] = 0

    @pytest.mark.parametrize('bc_lured', [COG_LVL1], indirect=['bc_lured'])
    def test_battle_toon_viable_attacks(self, bt_trapa: BattleToon, bc_lured: BattleCog):
        """
        Verify Trapa has 1 viable Attacks, and none are Heal/Lure/Trap, against a lured Flunky.

        Viable attacks only consider Gags which provide a reward.
            Reward is given when the Gag.level is lower than the Cog.
        """
        viable_attacks = bt_trapa.get_viable_attacks(target=bc_lured)
        assert len(viable_attacks) == 1
        assert viable_attacks[0].name == GAG.CUPCAKE.name
        assert viable_attacks[0].gag.track == GAG.CUPCAKE.track == TRACK.THROW

        bt_trapa.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10
        bt_trapa.entity.gags.gag_count[TRACK.LURE][GAG.SMALL_MAGNET.level] = 10
        bt_trapa.entity.gags.gag_count[TRACK.HEAL][GAG.FEATHER.level] = 10

        viable_attacks = bt_trapa.get_viable_attacks(target=bc_lured)
        assert all([atk.gag.track not in [TRACK.HEAL, TRACK.LURE, TRACK.TRAP] for atk in viable_attacks])  # noqa
        assert all([atk.gag.track in [TRACK.THROW, TRACK.SQUIRT] for atk in viable_attacks])
        assert len(viable_attacks) == 2

        assert viable_attacks[0].name == GAG.CUPCAKE.name
        assert viable_attacks[0].gag.track == GAG.CUPCAKE.track == TRACK.THROW

        bt_trapa.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0
        bt_trapa.entity.gags.gag_count[TRACK.LURE][GAG.SMALL_MAGNET.level] = 0
        bt_trapa.entity.gags.gag_count[TRACK.HEAL][GAG.FEATHER.level] = 0


class TestBattleToonTrapaGetAttacksTrappedBattleCog:

    @pytest.mark.parametrize('bc_trapped', [COG_LVL1], indirect=['bc_trapped'])
    def test_battle_toon_gag_is_possible(self, bt_trapa: BattleToon, bc_trapped: BattleCog):
        """
        Verify Trapa has only 25 possible Gags against a trapped lvl 1 Flunky.
            NOTE: #25 b/c `bt_trapa` has 34 total Gags, but 9 cannot possibly be used against
                  the trapped lvl 1 Flunky:
                    - 6 Toon-Up Gags are impossible attacks against the Flunky
                    - 3 Trap Gags are impossible attacks against the trapped Flunky
        Gag possibility does NOT take into account the current quantity of the Gag (Gag.count)
        Gag possibility is True if the Gag is unlocked, not a Heal Gag, not a Lure Gag when the
            target is lured/trapped, and not a Trap Gag when the target is lured/trapped.
        """
        # expected number is 6 unlocked Heal gags
        num_heal_gags = TRAPA_EXPECTED_TRACK_LEVELS[TRACK.HEAL] + 1
        # expected number is 3 unlocked Trap gags
        num_trap_gags = TRAPA_EXPECTED_TRACK_LEVELS[TRACK.TRAP] + 1
        sum_num_gags = num_heal_gags + num_trap_gags

        expected_num_gags = TRAPA_EXPECTED_UNLOCKED_GAGS - sum_num_gags
        assert expected_num_gags == 25

        possible_gags = []
        for gag in bt_trapa.entity.gags.unlocked_gags:
            if bt_trapa._gag_is_possible(gag=gag, target=bc_trapped):
                assert gag.track not in [TRACK.HEAL, TRACK.TRAP]
                possible_gags.append(gag)
        assert len(possible_gags) == expected_num_gags

    @pytest.mark.parametrize('bc_trapped', [COG_LVL1], indirect=['bc_trapped'])
    def test_battle_toon_gag_is_viable(self, bt_trapa: BattleToon, bc_trapped: BattleCog):
        """
        Verify Trapa has only 4 viable Gags, and none are Heal/Trap, against a trapped Flunky.
            NOTE: #4 because `bt_trapa` has 6 unlocked lvl 1 Gags, but 2 cannot possibly be used
                  against the lvl 1 Flunky:
                    - 1 Toon-Up Gag (lvl 0 Toon-Up) is an impossible attack against the Flunky
                    - 1 Trap Gag (lvl 0 Trap) is an impossible attack against the trapped Flunky
        Gag viability does NOT take into account the current quantity of the Gag (Gag.count)

        Gag viability is True if the Gag is possible (see above) and a lower level than the target.
        """
        viable_gags = []
        for gag in bt_trapa.entity.gags.unlocked_gags:
            if bt_trapa._gag_is_viable(gag=gag, target=bc_trapped):
                assert gag.track not in [TRACK.HEAL, TRACK.TRAP]
                viable_gags.append(gag)
        assert len(viable_gags) == 4

    @pytest.mark.parametrize('bc_trapped', [COG_LVL1], indirect=['bc_trapped'])
    def test_battle_toon_possible_attacks(self, bt_trapa: BattleToon, bc_trapped: BattleCog):
        """
        Verify Trapa has 15 possible Attacks, and none are Heal/Trap, against a trapped Flunky.

        Possible attacks only consider if the Gag is unlocked and Gag.count > 0.
        Reward (given when the Gag.level is lower than the Cog), is not considered when
            categorizing possible attacks.
        """
        possible_attacks = bt_trapa.get_possible_attacks(target=bc_trapped)
        assert possible_attacks != []
        assert len(possible_attacks) == 15

        bt_trapa.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10
        bt_trapa.entity.gags.gag_count[TRACK.HEAL][GAG.FEATHER.level] = 10

        possible_attacks = bt_trapa.get_possible_attacks(target=bc_trapped)
        assert all([
            atk.gag.track not in [TRACK.HEAL, TRACK.TRAP]
            for atk in possible_attacks
        ])
        assert len(possible_attacks) == 16

        bt_trapa.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0
        bt_trapa.entity.gags.gag_count[TRACK.HEAL][GAG.FEATHER.level] = 0

    @pytest.mark.parametrize('bc_trapped', [COG_LVL1], indirect=['bc_trapped'])
    def test_battle_toon_viable_attacks(self, bt_trapa: BattleToon, bc_trapped: BattleCog):
        """
        Verify Trapa has 2 viable Attacks, and none are Heal/Trap, against a trapped Flunky.

        Viable attacks only consider Gags which provide a reward.
            Reward is given when the Gag.level is lower than the Cog.
        """
        viable_attacks = bt_trapa.get_viable_attacks(target=bc_trapped)
        assert len(viable_attacks) == 2
        assert viable_attacks[0].name == GAG.ONE_BILL.name
        assert viable_attacks[0].gag.track == TRACK.LURE
        assert viable_attacks[1].name == GAG.CUPCAKE.name
        assert viable_attacks[1].gag.track == TRACK.THROW

        bt_trapa.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 10
        bt_trapa.entity.gags.gag_count[TRACK.LURE][GAG.SMALL_MAGNET.level] = 10
        bt_trapa.entity.gags.gag_count[TRACK.HEAL][GAG.FEATHER.level] = 10

        viable_attacks = bt_trapa.get_viable_attacks(target=bc_trapped)
        assert all([atk.gag.track not in [TRACK.HEAL, TRACK.TRAP] for atk in viable_attacks])
        assert all([atk.gag.track in [TRACK.LURE, TRACK.THROW, TRACK.SQUIRT] for atk in viable_attacks])  # noqa
        assert len(viable_attacks) == 3

        assert viable_attacks[0].name == GAG.ONE_BILL.name
        assert viable_attacks[1].name == GAG.CUPCAKE.name
        assert viable_attacks[2].name == GAG.SQUIRTING_FLOWER.name

        bt_trapa.entity.gags.gag_count[TRACK.SQUIRT][GAG.SQUIRTING_FLOWER.level] = 0
        bt_trapa.entity.gags.gag_count[TRACK.LURE][GAG.SMALL_MAGNET.level] = 0
        bt_trapa.entity.gags.gag_count[TRACK.HEAL][GAG.FEATHER.level] = 0


def verify_all_attack_reward_values(rc: RewardCalculator, toon: BattleToon, target: BattleCog):
    """Verify all attack.reward values are equivalent to the expected attack reward"""
    assert all([
        attack.reward == get_expected_reward(toon_attack=attack, rc=rc)
        for attack in toon.get_possible_attacks(target=target)
    ])


def verify_possible_attack_reward_levels(toon: BattleToon, target: BattleCog):
    """Verify, based on the possible attack's level, if the reward is less/greater than 0"""
    for attack in toon.get_possible_attacks(target=target):
        if attack.gag.level >= attack.target_cog.level:
            assert attack.reward < 0
        else:
            assert attack.reward > 0


def verify_viable_attack_reward_levels(toon: BattleToon, target: BattleCog):
    """Verify all viable attack.reward greater than 0"""
    assert all([
        attack.reward > 0
        for attack in toon.get_viable_attacks(target=target)
    ])


class TestBattleToonAstroGetAttacksRewards:
    """Verify attack rewards for Toons in a default Battle"""

    @pytest.fixture(params=[COG_LVL1, COG_LVL4, COG_LVL7])
    def battle(self, toon_astro: Toon, request: Cog) -> Battle:
        battle = Battle()
        battle.add_toon(new_toon=toon_astro)
        battle.add_cog(new_cog=request.param)
        return battle

    @staticmethod
    def verify_all_attack_reward_values(battle: Battle):
        """Verify all attack.reward values are equivalent to the expected attack reward"""
        assert battle.cogs != []
        assert battle.toons != []

        for toon in battle.toons:
            for target in battle.cogs:
                verify_all_attack_reward_values(rc=battle.reward_calculator,
                                                toon=toon, target=target)

    @staticmethod
    def verify_possible_attack_reward_levels(battle: Battle):
        """Verify, based on the possible attack's level, if the reward is less/greater than 0"""
        assert battle.cogs != []
        assert battle.toons != []

        for toon in battle.toons:
            for target in battle.cogs:
                verify_possible_attack_reward_levels(toon=toon, target=target)

    @staticmethod
    def verify_viable_attack_reward_levels(battle: Battle):
        """Verify all viable attack.reward greater than 0"""
        assert battle.cogs != []
        assert battle.toons != []

        for toon in battle.toons:
            for target in battle.cogs:
                verify_viable_attack_reward_levels(toon=toon, target=target)

    def test_all_attack_reward_values(self, battle: Battle):
        self.verify_all_attack_reward_values(battle=battle)

    def test_possible_attack_rewards(self, battle: Battle):
        self.verify_possible_attack_reward_levels(battle=battle)

    def test_viable_attack_rewards(self, battle: Battle):
        self.verify_viable_attack_reward_levels(battle=battle)


class TestBattleToonAstroGetAttacksRewardsBuilding(TestBattleToonAstroGetAttacksRewards):
    """Verify attack rewards for Toons in Battle within a building"""

    @pytest.fixture(params=[COG_LVL1, COG_LVL4, COG_LVL7])
    def battle(self, toon_astro: Toon, battle_building: Battle, request: BattleCog) -> Battle:
        battle_building.add_toon(new_toon=toon_astro)
        battle_building.add_cog(new_cog=request.param)
        return battle_building

    def test_all_attack_reward_values(self, battle: Battle):
        self.verify_all_attack_reward_values(battle=battle)

    def test_possible_attack_rewards(self, battle: Battle):
        self.verify_possible_attack_reward_levels(battle=battle)

    def test_viable_attack_rewards(self, battle: Battle):
        self.verify_viable_attack_reward_levels(battle=battle)


class TestBattleToonAstroGetAttacksRewardsBuildingInvasion(TestBattleToonAstroGetAttacksRewards):
    """Verify attack rewards for Toons in Battle within a building during an invasion"""

    @pytest.fixture(params=[COG_LVL1, COG_LVL4, COG_LVL7])
    def battle(self, toon_astro: Toon, battle_building_invasion: Battle,
               request: BattleCog) -> Battle:
        battle_building_invasion.add_toon(new_toon=toon_astro)
        battle_building_invasion.add_cog(new_cog=request.param)
        return battle_building_invasion

    def test_all_attack_reward_values(self, battle: Battle):
        self.verify_all_attack_reward_values(battle=battle)

    def test_possible_attack_rewards(self, battle: Battle):
        self.verify_possible_attack_reward_levels(battle=battle)

    def test_viable_attack_rewards(self, battle: Battle):
        self.verify_viable_attack_reward_levels(battle=battle)
