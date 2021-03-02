from ..fixtures.cog_fixtures import cog_flunky as cogf
from ..fixtures.toon_fixtures import toon_astro
from ...CogGlobals import (
    get_cog_attack, get_cog_attacks_all_levels, pick_cog_attack
    )
import pytest


@pytest.mark.parametrize('cogf', [0, 1, 2, 3, 4], indirect=True)
class TestCogAttack:

    @pytest.mark.parametrize('exp_attack_index,exp_attack_name', [
        (0, 'PoundKey'), (1, 'Shred'), (2, 'ClipOnTie')])
    def test_cog_get_cog_attack(self, cogf, exp_attack_index, exp_attack_name):
        cog_attack = get_cog_attack(cog_key=cogf.key,
                                    relative_level=cogf.relative_level,
                                    attack_index=exp_attack_index)
        assert type(cog_attack) == dict
        assert cog_attack['name'] == exp_attack_name
        assert cog_attack['id'] == exp_attack_index

    def test_cog_pick_attack_index_random(self, cogf):
        attack_choices = get_cog_attacks_all_levels(cog_key=cogf.key)
        attack_index = pick_cog_attack(attack_choices=attack_choices,
                                       relative_level=cogf.relative_level)
        assert attack_index in range(len(attack_choices))

    def test_cog_pick_attack_random(self, cogf):
        attack_choices = get_cog_attacks_all_levels(cog_key=cogf.key)
        attack_index = pick_cog_attack(attack_choices=attack_choices,
                                       relative_level=cogf.relative_level)
        cog_attack = get_cog_attack(cog_key=cogf.key,
                                    relative_level=cogf.relative_level,
                                    attack_index=attack_index)
        assert type(cog_attack) == dict

    @pytest.mark.parametrize('attack_index', [0, 1, 2])
    def test_cog_attack_damages_toon(self, cogf, toon_astro, attack_index):
        cog_attack = get_cog_attack(cog_key=cogf.key,
                                    relative_level=cogf.relative_level,
                                    attack_index=attack_index)

        attack_dmg = cog_attack['hp']

        print(f"\nBEFORE: hp {toon_astro.hp}")
        print(f"Cog \"{cogf.name}\" (lvl {cogf.level}) attacks {toon_astro.hp}"
              f"hp Toon \"Astro\" with {attack_dmg} damage attack "
              f"\"{cog_attack['name']}\"")
        cogf.do_attack(target=toon_astro, amount=attack_dmg)
        print(f"AFTER: {toon_astro.hp}")
        print(cog_attack['name'], cog_attack['id'], cog_attack['hp'])

    # TODO Create test for cog attack damaging multiple toons
    # NOTE: Must be done with Yesman fixture, attack_name='Synergy'
