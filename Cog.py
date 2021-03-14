from random import randint

from .CogGlobals import get_actual_from_relative_level, get_cog_vitals
from .Entity import Entity
from .Exceptions import InvalidCogAttackTarget


class Cog(Entity):
    def __init__(self, key, name, relative_level=0):
        self.vitals = get_cog_vitals(
            cog_key=key, relative_level=relative_level
            )
        super().__init__(name=name, hp=self.vitals['hp'])

        self.key = key
        self.attacks = self.vitals['attacks']
        self.defense = self.vitals['def']
        # ! Relative level should be in range [0,4]
        self.relative_level = relative_level
        self.level = get_actual_from_relative_level(
            cog_key=key, relative_level=relative_level
            )

    # TODO Make this follow Toon's `do_attack`, add  atk_indx
    def do_attack(self, target, amount: int):
        """Perform an attack on a Toon, given an attack damage

        Args:
            target (Toon): Toon object that is going to be attacked
            amount (int): Attack's damage amount

        Returns:
            int: 0 if the attack misses, 1 if it hits
        """
        from .Toon import Toon

        if type(target) != Toon:
            raise InvalidCogAttackTarget

        if target.is_defeated():
            raise InvalidCogAttackTarget

        # TODO Add chance_to_hit
        attack_hit = super().do_attack(target=target, amount=amount)
        return attack_hit

    def get_attack(self, attack_name: str) -> dict:
        """Return dictionary containing Cog attack information, given an index#

        Args:
            attack_name (str, optional): Attack name as seen in COG_ATTACKS or
                the `get_cog_attacks_all_levels` function

            Example of valid input ::
                <'PoundKey'|'Shred'|'ClipOnTie'>

        Returns:
            dict: Dictionary containing all attributes of a single Cog's attack

            Example output for attack_name='PoundKey' ::
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
    def pick_attack(self, attack_name: str='') -> int:
        """Return attack_index of cog attack from cog.attacks, a pseudo-random
            attack index is returned by default unless the `attack_name`
            argument is provided

        Args:
            attack_name (str, optional): Attack name as seen in COG_ATTACKS or
                the `get_cog_attacks_all_levels` function

            Example of valid input ::
                <'PoundKey'|'Shred'|'ClipOnTie'>  # Returns <0|1|2>

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
