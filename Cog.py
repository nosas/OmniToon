from random import randint
from .Entity import Entity
from .CogGlobals import (
    get_cog_vitals, get_actual_from_relative_level, ATK_IDX_FREQ)


class Cog(Entity):
    def __init__(self, key, name, relative_level=0):
        self.key = key
        self.name = name
        self.vitals = get_cog_vitals(
            cog_key=key, relative_level=relative_level
            )
        self.attacks = self.vitals['attacks']
        self.hp = self.vitals['hp']
        # ! Relative level should be in range [0,4]
        self.relative_level = relative_level
        self.level = get_actual_from_relative_level(
            cog_key=key, relative_level=relative_level
            )
        super().__init__(name=self.name, hp=self.hp)

    def get_attack(self, attack_name: str) -> dict:
        """Return dictionary containing Cog attack information, given an index#

        Args:
            attack_name (str):

        Returns:
            dict: Dictionary containing all attributes of a single Cog's attack
        Example ::
            {
                'acc': 80,
                'animName': 'phone',
                'freq': 40,
                'hp': 3,
                'id': 0,
                'name': 'PoundKey',
                'target': 2  # ATK_TGT_SINGLE=1, ATK_TGT_GROUP=2
            }
        """
        assert attack_name in self.attacks
        return self.attacks[attack_name]

    # TODO: Create `pick_target` function to choose a target when vs 2+ toons
    # ! Need to write tests for this method
    def pick_attack(self, attack_name='') -> int:
        """Return attack_index of cog attack from cog.attacks, a
            pseudo-random attack index is returned by default unless the
            `attack_name` argument is provided

        Args:
            attack_name (str, optional): Attack name as seen in COG_ATTACKS or
                the `get_cog_attacks_all_levels` function
                    example input ::
                        <'PoundKey'|'Shred'|'ClipOnTie'>
        Returns:
            int: Index of the Cog attack
        """
        if attack_name:
            assert attack_name in self.attacks
            return self.attacks.index(attack_name)

        attack_index = None
        rand_num = randint(0, 99)
        count = 0
        cur_index = 0

        for name in self.attacks:
            attack = self.attacks[name]
            atk_frequency = attack['freq']
            count = count + atk_frequency
            if rand_num < count:
                attack_index = cur_index
                break
            cur_index = cur_index + 1
        return attack_index
