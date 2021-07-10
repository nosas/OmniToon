from dataclasses import dataclass, field
from random import choice as rand_choice
from random import randint
from typing import Optional, Tuple

from .Attack import Attack
from .CogGlobals import COG_ATTRIBUTES, get_cog_vitals
from .Entity import Entity
from .Exceptions import (CogAlreadyTrappedError, CogLuredError,
                         InvalidCogAttackTarget, InvalidRelativeLevel)
from .Gag import Gag


class CogAttack(Attack):

    def __repr__(self) -> str:
        return str(self.__dict__)


@dataclass
class Cog(Entity):

    key: str
    relative_level: Optional[int] = field(default=0)

    # Prevent needing to pass in Attack's required arguments
    # Instead, pass in the required arguments during __post_init__()
    name: str = field(init=False)
    hp: int = field(init=False)
    # # For testing purposes. See `test_cog_attack_damages_multiple_toons`
    manual_atk: CogAttack = field(init=False, default=None)

    # TODO (??) Create CogStates
    _is_lured: bool = field(init=False, default=False)
    _is_trapped: bool = field(init=False, default=False)
    _trap: Tuple[Entity, Gag] = field(init=False, default=None)

    def __post_init__(self):
        self.vitals = get_cog_vitals(cog_key=self.key,
                                     relative_level=self.relative_level)
        self.name = self.vitals['name']
        self.hp_max = self.vitals['hp']

        super().__init__(name=self.name, hp=self.hp_max)
        self.attacks = self.vitals['attacks']
        self.defense = self.vitals['def']
        self.level = self.vitals['level']

    # ! This will cause issues if 2+ Toons have the same name
    def __hash__(self) -> int:
        return hash((self.name, self.key))

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

    # TODO #40, `choose_target` method to choose a target when vs 2+ toons
    # TODO #39, Need to write tests for this method
    def choose_attack(self, attack_name: str = '') -> CogAttack:
        """Return Attack obj containing Cog attack information from
            self.attacks, a pseudo-random Attack is returned by default
            unless the `attack_name` argument is provided

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

    def do_attack(self, target, attack: CogAttack) -> bool:
        """Perform an attack on a Toon, given an attack damage

        Args:
            target (Toon): Toon object that is going to be attacked
            attack (CogAttack): Attack's damage attack

        Returns:
            bool: False if the attack misses, True if it hits
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
        attack_hit = Entity.do_attack(self, target=target, attack=attack)
        return attack_hit

    def get_attack(self, attack_name: str) -> CogAttack:
        """Return Attack obj containing Cog attack info, given an attack name

        Args:
            attack_name (str, optional): Attack name as seen in COG_ATTACKS or
                the `get_cog_attacks_all_levels` function

            Example of valid input ::
                <'PoundKey'|'Shred'|'ClipOnTie'>

        Returns:
            CogAttack: All attributes of the Cog's attack

            Example output for attack_name='PoundKey' ::
                {
                    'acc': 80,
                    'damage': 3,
                    'name': 'PoundKey',
                    'target': 2  # ATK_TGT_SINGLE=1, ATK_TGT_MULTI=2
                }
        """
        assert (attack_name != '')
        valid_name = [attack_name == attack['name'] for attack in self.attacks]
        assert valid_name.count(True) == 1
        attack_idx = valid_name.index(True)
        attack = self.attacks[attack_idx]
        return CogAttack(name=attack['name'], damage=attack['damage'],
                         accuracy=attack['acc'], target=attack['target'])


def get_random_cog() -> Cog:

    cog_key = rand_choice(list(COG_ATTRIBUTES.keys()))
    relative_level = randint(0, 4)
    return Cog(key=cog_key,  relative_level=relative_level)
