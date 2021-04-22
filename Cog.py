from random import choice as rand_choice
from random import randint

from .CogGlobals import COG_ATTRIBUTES, get_cog_vitals
from .Entity import Entity
from .Exceptions import (CogAlreadyTrappedError, CogLuredError,
                         InvalidCogAttackTarget, InvalidRelativeLevel)


class Cog(Entity):
    def __init__(self, key, name, relative_level=0, hp=-1):
        # ! Relative level should be in range [0,4]
        self.relative_level = relative_level
        self.vitals = get_cog_vitals(
            cog_key=key, relative_level=relative_level
            )
        super().__init__(name=name, hp=hp if (hp != -1) else self.vitals['hp'])

        self.key = key
        self.attacks = self.vitals['attacks']
        self.defense = self.vitals['def']
        self.hp_max = self.vitals['hp']
        self.level = self.vitals['level']
        # TODO (??) Create CogStates
        self._is_lured = False
        self._is_trapped = False
        self._trap = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'lvl {self.level} "{self.name}" ({self.hp}/{self.hp_max}hp)'

    @property
    def is_lured(self) -> bool:
        return self._is_lured

    @is_lured.setter
    def is_lured(self, new_is_lured: bool) -> None:
        assert type(new_is_lured) == bool
        print(f"                [>] is_lured : {self.is_lured} -> "
              f"{new_is_lured} on {self}")
        if new_is_lured and self.is_lured:
            raise CogLuredError("Can't Lure a Cog that's already Lured")
        self._is_lured = new_is_lured

    @property
    def is_trapped(self) -> bool:
        return self._is_trapped

    @is_trapped.setter
    def is_trapped(self, new_is_trapped: bool) -> None:
        assert type(new_is_trapped) == bool
        print(f"                [>] is_trapped : {self.is_trapped} -> "
              f"{new_is_trapped} on {self}")
        if new_is_trapped:
            # If two or more Trap gags are deployed in front of the same cog,
            # the gags will "cancel" each other out and will render a waste.
            if self.is_trapped:
                raise CogAlreadyTrappedError
            # ! Trap gags cannot be placed if a Cog is already lured
            if self.is_lured:
                raise CogLuredError
            self._is_trapped = True
        else:
            self._is_trapped = False
            print(f"                [>] self.trap : {(self.trap)} -> None on {self}")  # noqa
            self._trap = None

    @property
    # def trap(self) -> tuple[Toon, Gag]:
    def trap(self) -> tuple:
        return self._trap

    @trap.setter
    def trap(self, toon_and_gag_trap) -> None:
        assert type(toon_and_gag_trap) == tuple
        assert len(toon_and_gag_trap) == 2

        from .Gag import Gag
        from .Toon import Toon

        toon = toon_and_gag_trap[0]
        gag_trap = toon_and_gag_trap[1]
        assert type(toon) == Toon
        assert type(gag_trap) == Gag
        print(f"                [>] self.trap : {(self.trap)} -> ({toon}, "
              f"{gag_trap}) on {self}")
        self._trap = (toon, gag_trap)

    @property
    def relative_level(self):
        return self._relative_level

    @relative_level.setter
    def relative_level(self, new_rel_lvl):
        if new_rel_lvl not in range(5):
            raise InvalidRelativeLevel
        self._relative_level = new_rel_lvl

    # TODO #40, `choose_target` method to choose a target when vs 2+ toons
    # TODO #39, Need to write tests for this method
    def choose_attack(self, attack_name: str = '') -> int:
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
        if attack_name == '':
            rand_num = randint(0, 99)
            count = 0
            for attack_dict in self.attacks:
                attack_name = attack_dict['name']
                attack_freq = attack_dict['freq']
                count = count + attack_freq
                if rand_num < count:
                    break
        return self.get_attack(attack_name=attack_name)

        # return attack['id']

    # TODO #41, Make this follow Toon's `do_attack`, add atk_indx
    def do_attack(self, target, amount: int):
        """Perform an attack on a Toon, given an attack damage

        Args:
            target (Toon): Toon object that is going to be attacked
            amount (int): Attack's damage amount

        Returns:
            int: 0 if the attack misses, 1 if it hits
        """
        # Have to import Toon here due to circular import issue when importing
        # Toon at the top of the file
        from .Toon import Toon

        if type(target) != Toon:
            raise InvalidCogAttackTarget(f"{self}'s attack target ({target}) "
                                         "must be a Toon")
        # #52, skip Cog attack if lured
        if self.is_lured:
            print(f"            [-] Cog `do_attack()` Skip lured {self}")
            return False

        # TODO #10, add chance_to_hit
        attack_hit = Entity.do_attack(self, target=target, amount=amount)
        return attack_hit

    # TODO #41, return a CogAttack object instead of dict?
    def get_attack(self, attack_name: str = '') -> dict:
        """Return dictionary containing Cog attack information, given an index#

        Args:
            attack_name (str, optional): Attack name as seen in COG_ATTACKS or
                the `get_cog_attacks_all_levels` function
            attack_idx (int, optional): Attack index for attacksseen in
                COG_ATTACKS or the `get_cog_attacks_all_levels` function

            Example of valid input ::
                <'PoundKey'|'Shred'|'ClipOnTie'>

        Returns:
            dict: Dictionary containing all attributes of a single Cog's attack

            Example output for attack_name='PoundKey' ::
                {
                    'acc': 80,
                    'freq': 40,
                    'hp': 3,
                    'id': 0,
                    'name': 'PoundKey',
                    'target': 2  # ATK_TGT_SINGLE=1, ATK_TGT_GROUP=2
                }
        """
        assert (attack_name != '')
        valid_name = [attack_name == attack['name'] for attack in self.attacks]
        assert valid_name.count(True) == 1
        attack_idx = valid_name.index(True)
        return self.attacks[attack_idx]


def get_random_cog() -> Cog:

    cog_key = rand_choice(list(COG_ATTRIBUTES.keys()))
    cog_name = COG_ATTRIBUTES[cog_key]['name']
    relative_level = randint(0, 4)
    return Cog(key=cog_key, name=cog_name, relative_level=relative_level)
