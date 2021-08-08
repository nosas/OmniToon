import pytest

from ...Battle import BattleCog, BattleToon
from ...Exceptions import NoValidAttacksError
from ...Factory import BattleCogFactory, CogFactory
from ...Gag import Gag
from ...GagGlobals import GAG, TRACK
from ...Toon import Toon


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
BC_LVL4 = BattleCogFactory().get_battle_cog(battle_id=BATTLE_ID, entity=COG_LVL4)
BC_LVL7 = BattleCogFactory().get_battle_cog(battle_id=BATTLE_ID, entity=COG_LVL7)
# Default Toon-specific global variables
NAME_TOON = 'Mickey'
TOON = Toon(name=NAME_TOON)
BT = BattleToon(battle_id=BATTLE_ID, entity=TOON)


class TestBattleToonDefaultChooseAttack:

    @pytest.mark.parametrize('target_cog', [BC_LVL1, BC_LVL4, BC_LVL7])
    def test_battle_toon_choose_attack_fail(self, bt: BattleToon, target_cog: BattleCog):
        """Verify the default BattleToon has no available Attacks against a BattleCog"""
        with pytest.raises(NoValidAttacksError):
            bt.choose_attack(target=target_cog)

    @pytest.mark.parametrize('target_cog', [BC_LVL1, BC_LVL4, BC_LVL7])
    def test_battle_toon_choose_attack(self, bt: BattleToon, target_cog: BattleCog,
                                       expected_gag: Gag = GAG.SQUIRTING_FLOWER):
        """Restock the Default Toon's Squirt Gag and verify the BattleToon chooses it over Drop"""
        # TODO Add `restock` function to easily restock a Gag
        # bt.entity.gags.gag_count[GAG.CUPCAKE.track][GAG.CUPCAKE.level] = 1
        bt.entity.gags.gag_count[GAG.FLOWER_POT.track][GAG.FLOWER_POT.level] = 1
        bt.entity.gags.gag_count[expected_gag.track][expected_gag.level] = 1

        chosen_gag = bt.choose_attack(target=target_cog).gag
        expected_gag = bt.entity.gags.get_gag(track=expected_gag.track,
                                              level=expected_gag.level)
        assert chosen_gag == expected_gag

        bt.entity.gags.gag_count[GAG.FLOWER_POT.track][GAG.FLOWER_POT.level] = -1
        bt.entity.gags.gag_count[expected_gag.track][expected_gag.level] = 0


class TestBattleToonAstroChooseAttack:

    @pytest.mark.parametrize('target_cog,expected_gag', [(BC_LVL1, GAG.TEN_BILL),
                                                         (BC_LVL4, GAG.WHOLE_FRUIT_PIE),
                                                         (BC_LVL7, GAG.PRESENTATION)])
    def test_battle_toon_choose_attack(self, bt_astro: BattleToon,
                                       target_cog: BattleCog, expected_gag: Gag):
        """Verify Astro chooses the highest-rewarding Attack against different leveled BattleCogs"""
        chosen_gag = bt_astro.choose_attack(target=target_cog).gag
        expected_astro_gag = bt_astro.entity.gags.get_gag(track=expected_gag.track,
                                                          level=expected_gag.level)
        assert chosen_gag == expected_astro_gag


class TestBattleToonTrapaChooseAttack:

    @pytest.mark.parametrize('target_cog,expected_gag', [
                             (BC_LVL1, GAG.from_tuple((TRACK.TRAP, 0))),
                             (BC_LVL4, GAG.from_tuple((TRACK.THROW, 3))),
                             (BC_LVL7, GAG.from_tuple((TRACK.LURE, 6)))])
    def test_battle_toon_choose_attack(self, bt_trapa: BattleToon,
                                       target_cog: BattleCog, expected_gag: Gag):
        """Verify Trapa chooses the highest-rewarding Attack against different leveled BattleCogs"""
        chosen_gag = bt_trapa.choose_attack(target=target_cog).gag
        expected_trapa_gag = bt_trapa.entity.gags.get_gag(track=expected_gag.track,
                                                          level=expected_gag.level)
        assert chosen_gag == expected_trapa_gag
