import pytest

from ...Attack import ATK_TGT_SINGLE, Attack
from ...CogGlobals import (get_cog_attack, get_cog_attacks_all_levels,
                           pick_cog_attack)
from ...Exceptions import InvalidCogAttackTarget
from ..fixtures.cog_fixtures import cog_flunky as cogf
from ..fixtures.toon_fixtures import toon_astro


# TODO create TestCogAttack, test against the Cog's methods instead of Globals
# TODO test `pick_cog_attack` with valid and invalid arguments for attack_name
@pytest.mark.parametrize('cogf', [0, 1, 2, 3, 4], indirect=True)
class TestCogGlobalAttack:

    dummy_atk = Attack(name='dummy', damage=10, accuracy=100,
                       target=ATK_TGT_SINGLE)

    # TODO Move to TestCogAttack when its created...
    def test_attack_target_cog_fail(self, cogf):
        """Verify Cog's `do_attack` raises InvalidCogAttackTarget when
        trying to attack a non-Toon object

        Args:
            cogf (Cog): Flunky Cog fixture
        """
        with pytest.raises(InvalidCogAttackTarget):
            attack_hit = cogf.do_attack(target=cogf, attack=self.dummy_atk)
            assert not attack_hit

    # TODO Move to TestCogAttack when its created...
    def test_attack_target_defeated_fail(self, cogf):
        """Verify Cog's `do_attack` raises InvalidCogAttackTarget when
        trying to attack a defeated Toon (Toon.hp <= 0) object

        Args:
            cogf (Cog): Flunky Cog fixture
        """
        with pytest.raises(InvalidCogAttackTarget):
            cogf.hp = 0
            attack_hit = cogf.do_attack(target=cogf, attack=self.dummy_atk)
            assert not attack_hit

    @pytest.mark.parametrize('exp_attack_index,exp_attack_name', [
        (0, 'PoundKey'), (1, 'Shred'), (2, 'ClipOnTie')])
    def test_cog_get_cog_attack(self, cogf, exp_attack_index, exp_attack_name):
        """Verify `get_cog_attack` output matches the expected Flunky's attack
        dictionary and contains the expected attack indexes and names

        Args:
            cogf (Cog): Flunky Cog fixture
            exp_attack_index (int): Index number for the expected Cog attack
            exp_attack_name (str): Name of expected Cog attack
        """
        cog_attack = get_cog_attack(cog_key=cogf.key,
                                    relative_level=cogf.relative_level,
                                    attack_index=exp_attack_index)
        # ? Should I create a static expected cog_attack dictionary here?
        assert type(cog_attack) == dict
        assert cog_attack['name'] == exp_attack_name
        assert cog_attack['id'] == exp_attack_index

    # ! How do we check if it's actually actually returning a random index?
    def test_cog_choose_attack_index_random(self, cogf):
        """Verify `pick_cog_attack` returns an attack_index within the
        Flunky's attack_index range

        Args:
            cogf (Cog): Flunky Cog fixture
        """
        attack_choices = get_cog_attacks_all_levels(cog_key=cogf.key)
        attack_index = pick_cog_attack(attack_choices=attack_choices,
                                       relative_level=cogf.relative_level)
        assert attack_index in range(len(attack_choices))

    def test_cog_choose_attack_random(self, cogf):
        """Verify `get_cog_attack` returns a valid Cog attack dictionary when
        passing in the `random_attack_idx` obtained from `pick_cog_attack`

        Args:
            cogf (Cog): Flunky Cog fixture
        """
        attack_choices = get_cog_attacks_all_levels(cog_key=cogf.key)
        random_attack_idx = pick_cog_attack(attack_choices=attack_choices,
                                            relative_level=cogf.relative_level)
        cog_attack = get_cog_attack(cog_key=cogf.key,
                                    relative_level=cogf.relative_level,
                                    attack_index=random_attack_idx)
        assert type(cog_attack) == dict
        # ! More validation needs to be done here, maybe against a static dict

    @pytest.mark.parametrize('attack_index', [0, 1, 2])
    def test_cog_attack_damages_toon(self, cogf, toon_astro, attack_index):
        cog_attack = get_cog_attack(cog_key=cogf.key,
                                    relative_level=cogf.relative_level,
                                    attack_index=attack_index)

        attack_dmg = cog_attack['damage']

        print(f"\nBEFORE: hp {toon_astro.hp}")
        print(f"Cog \"{cogf.name}\" (lvl {cogf.level}) attacks {toon_astro.hp}"
              f"hp Toon \"Astro\" with {attack_dmg} damage attack "
              f"\"{cog_attack['name']}\"")
        cogf.do_attack(target=toon_astro, attack=self.dummy_atk)
        print(f"AFTER: {toon_astro.hp}")
        print(cog_attack['name'], cog_attack['id'], cog_attack['damage'])
