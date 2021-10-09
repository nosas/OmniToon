from typing import List

import pytest

from ...Battle import Battle
from ...Cog import Cog
from ...Factory import CogFactory
from ...Gag import GAG, TRACK, Gag
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


class TestBattleAttackProcessor:
    """Verify AttackProcessor creation and attributes when adding/removing Cogs/Toons"""

    @pytest.fixture
    def battle(self, toon_astro: Toon) -> Battle:
        """Return a Battle object with 2 BattleToons"""
        battle = Battle()
        battle.add_toon(new_toon=toon_astro)
        return battle

    def test_battle_atkproc_creation(self, battle: Battle):
        """Verify AttackProcessor is created upon Battle instantiation"""
        assert battle.attack_processor.cogs == battle.cogs
        assert battle.attack_processor.toons == battle.toons

    def test_battle_atkproc_add_toon(self, battle: Battle, toon_trapa: Toon):
        """Verify AttackProcessor.toons is updated when a new Toon joins Battle"""
        battle.add_toon(new_toon=toon_trapa)
        assert battle.attack_processor.cogs == battle.cogs
        assert battle.attack_processor.toons == battle.toons

    def test_battle_atkproc_add_cog(self, battle: Battle):
        """Verify AttackProcessor.cogs is updated when a new Cog joins Battle"""
        battle.add_cog(new_cog=COG_LVL1)
        assert battle.attack_processor.cogs == battle.cogs
        assert battle.attack_processor.toons == battle.toons


class TestBattleAttackProcessorChooseToonAttacks:
    """Verify attack rewards for Toons in a default Battle"""

    @pytest.fixture
    def battle(self, toon_astro: Toon, toon_trapa: Toon) -> Battle:
        """Return a Battle object with 2 BattleToons"""
        battle = Battle()
        battle.add_toon(new_toon=toon_astro)
        battle.add_toon(new_toon=toon_trapa)
        return battle

    @pytest.mark.parametrize('cog,expected_gag', [(COG_LVL1, GAG.TEN_BILL),
                                                  (COG_LVL4, GAG.WHOLE_FRUIT_PIE),
                                                  (COG_LVL7, GAG.PRESENTATION)])
    def test_battle_atkproc_choose_toon_attack(self, battle: Battle, cog: Cog, expected_gag: Gag):
        """Verify BT Astro selects the expected Attack against different leveled Cogs"""
        battle.add_cog(new_cog=cog)
        battle.attack_processor.choose_toon_attacks()
        attacks = battle.attack_processor.attacks
        assert attacks[0][0] == battle.toons[0]
        assert attacks[0][1].gag.track == expected_gag.track
        assert attacks[0][1].gag.level == expected_gag.level

    @pytest.mark.parametrize(
        'cogs,expected_gags', [
            ([COG_LVL1, COG_LVL7], (GAG.PRESENTATION, GAG.PRESENTATION)),
            ([COG_LVL4, COG_LVL1], (GAG.from_tuple((TRACK.THROW, 3)), GAG.from_tuple((TRACK.THROW, 3)))),  # noqa
            ([COG_LVL7, COG_LVL4], (GAG.PRESENTATION, GAG.PRESENTATION))
        ]
    )
    def test_battle_atkproc_choose_toon_attack_multiple_cogs(self, battle: Battle, cogs: List[Cog],
                                                             expected_gags: List[Gag]):
        """Verify BattleToons select Attacks based on the highest leveled Battle Cog"""
        for cog in cogs:
            battle.add_cog(new_cog=cog)

        battle.attack_processor.choose_toon_attacks()
        attacks = battle.attack_processor.attacks
        for toon, attack, expected_gag in zip(battle.toons, attacks, expected_gags):
            assert attack[0] == toon
            assert attack[1].gag.track == expected_gag.track
            assert attack[1].gag.level == expected_gag.level

    @pytest.mark.parametrize(
        'cog,expected_gags', [
            (COG_LVL1, (GAG.from_tuple((TRACK.SOUND, 4)), GAG.from_tuple((TRACK.THROW, 0)))),
            (COG_LVL4, (GAG.from_tuple((TRACK.THROW, 3)), GAG.from_tuple((TRACK.THROW, 3)))),
            (COG_LVL7, (GAG.from_tuple((TRACK.SOUND, 5)), GAG.from_tuple((TRACK.SOUND, 5))))
        ]
    )
    def test_battle_atkproc_choose_toon_attack_lured_cog(self, battle: Battle, cog: Cog,
                                                         expected_gags: List[Gag]):
        """Verify BattleToons do not select Lure against a Lured Cog"""
        battle.add_cog(new_cog=cog)
        battle.cogs[0].is_lured = True

        battle.attack_processor.choose_toon_attacks()
        attacks = battle.attack_processor.attacks
        for toon, attack, expected_gag in zip(battle.toons, attacks, expected_gags):
            assert attack[0] == toon
            assert attack[1].gag.track != TRACK.LURE
            assert attack[1].gag.track == expected_gag.track
            assert attack[1].gag.level == expected_gag.level


class TestBattleAttackProcessorGroupAttacks:

    @pytest.fixture
    def battle(self, toon_astro: Toon) -> Battle:
        """Return a Battle object with 1 BattleToon"""
        battle = Battle()
        battle.add_toon(new_toon=toon_astro)
        return battle

    def test_battle_atkproc_group_attacks_no_cogs(self, battle: Battle):
        """
        Verify the BattleToon selects None as an Attack, and AttackProcessor
            can properly handle accepting None as input

        Manually select an Attack against a Cog and validate the format of
            `Battle.AttackProcessor.attacks_grouped`
        """
        assert battle.cogs == []

        battle.attack_processor.choose_toon_attacks()
        attacks = battle.attack_processor.attacks
        assert attacks == [(battle.toons[0], None)]

        grouped_attacks = battle.attack_processor.group_attacks(attacks=attacks)
        assert grouped_attacks is None
        print(grouped_attacks)

    # @pytest.mark.parametrize('cog,expected_gag', [(COG_LVL1, GAG.from_tuple((TRACK.DROP, 1)))])
    @pytest.mark.parametrize('cog,expected_gag', [(COG_LVL1, GAG.TEN_BILL)])
    def test_battle_atkproc_group_attacks_1cog(self, battle: Battle, cog: Cog,
                                               expected_gag: Gag):
        """
        Verify a single BattleToon's attacks are grouped properly

        Manually select an Attack against a Cog and validate the format of
            `Battle.AttackProcessor.attacks_grouped`
        """
        battle.add_cog(new_cog=cog)
        assert battle.cogs != []
        assert battle.cogs[0].entity == cog

        toon = battle.toons[0]
        expected_attack = toon.choose_manual_attack(target=battle.cogs[0], gag=expected_gag)
        battle.attack_processor.choose_toon_attacks()
        attacks = battle.attack_processor.attacks
        assert attacks == [(toon, expected_attack)]

        grouped_attacks = battle.attack_processor.group_attacks(attacks=attacks)
        assert grouped_attacks == {
            expected_gag.track: {
                battle.cogs[0].battle_id: [(toon, expected_attack)]
            }
        }
        print(grouped_attacks)
