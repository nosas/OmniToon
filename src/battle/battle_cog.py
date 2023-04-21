# TODO Look into Strategy design patterns for Toon decision making
# TODO #38 Different strategies: max_reward, fast_win_ignore_reward, survive..
# Pass: Clicking on PASS lets you skip your turn. Since Cogs will attack the
# Toon who has done him the most damage, you are less likely to be attacked
# if you choose Pass. This is a good strategy in a group battle if your Laff
# points are dangerously low.


from dataclasses import dataclass, field
from random import randint
from typing import Tuple

from src.core.cog import Cog
from src.core.entity import Entity
from src.core.exceptions import (
    CogAlreadyTrappedError,
    CogLuredError,
    InvalidCogAttackTarget,
)

from .attack import Attack
from .battle_entity import BattleEntity


@dataclass
class BattleCog(BattleEntity):
    entity: Cog

    # Initialize default values for all properties
    _entity: Entity = field(init=False, repr=False)
    _is_lured: bool = field(init=False, default=False)
    _is_trapped: bool = field(init=False, default=False)
    _trap: Tuple[BattleEntity, Attack] = field(init=False, default=(None, None))

    def _clear_trap(self) -> None:
        self._trap = None

    @property
    def entity(self) -> Cog:
        return self._entity

    @entity.setter
    def entity(self, new_entity: Cog) -> None:
        if not isinstance(new_entity, Cog):
            raise ValueError("BattleCog.entity must be of type Cog")
        self._entity = new_entity

    @property
    def is_lured(self) -> bool:
        return self._is_lured

    @is_lured.setter
    def is_lured(self, new_is_lured: bool) -> None:
        """Set the Cog's is_lured flag to True or False
        Args:
            new_is_lured (bool): True or False value to be set as the Cog's is_lured flag
        Raises:
            TypeError: `new_is_lured` is not a boolean value
            CogLuredError: The Cog is already lured and `new_is_lured` is True
        """
        if not isinstance(new_is_lured, bool):
            raise TypeError

        if new_is_lured and self.is_lured:
            raise CogLuredError("Can't Lure a Cog that's already Lured")
        print(
            f"                [>] is_lured : {self.is_lured} ->  {new_is_lured} on {self}"
        )
        self._is_lured = new_is_lured

    @property
    def is_trapped(self) -> bool:
        return self._is_trapped

    @is_trapped.setter
    def is_trapped(self, new_is_trapped: bool) -> None:
        """Set the Cog's is_trapped flag to True or False
        A Cog cannot be trapped when...
            - the Cog is lured
            - the Cog is trapped
        Args:
            new_is_trapped (bool): True or False value to be set as the Cog's is_trapped flag
        Raises:
            TypeError: `new_is_trapped` is not a boolean value
            CogAlreadyTrappedError: The Cog is already trapped and `new_is_trapped` is True
            CogLuredError: The Cog is lured and `new_is_trapped` is True
        """
        if not isinstance(new_is_trapped, bool):
            raise TypeError
        print(
            f"                [>] is_trapped : {self.is_trapped} -> "
            f"{new_is_trapped} on {self}"
        )
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
            print(
                f"                [>] self.trap : {(self.trap)} -> None on {self}"
            )  # noqa
            self._trap = None

    @property
    def key(self) -> str:
        return self.entity.key

    @property
    def level(self) -> int:
        return self.entity.level

    @property
    def relative_level(self) -> int:
        return self.entity.relative_level

    @property
    def trap(self) -> Tuple[BattleEntity, Attack]:
        return self._trap

    @trap.setter
    def trap(self, toon_and_gag_trap: Tuple[BattleEntity, Attack]) -> None:
        assert isinstance(toon_and_gag_trap, tuple)
        assert len(toon_and_gag_trap) == 2

        toon = toon_and_gag_trap[0]
        gag_trap = toon_and_gag_trap[1]
        assert isinstance(toon, BattleEntity)
        assert isinstance(gag_trap, Attack)
        print(
            f"                [>] self.trap : {self.trap} -> {toon_and_gag_trap} on {self}"
        )
        self._trap = toon_and_gag_trap

    # TODO #40, `choose_target` method to choose a target when vs 2+ toons
    # TODO #39, Need to write tests for this method
    def choose_action(self, attack_name: str = "") -> Attack:
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
        if attack_name == "":
            rand_num = randint(0, 99)
            count = 0
            for attack_dict in self.attacks:
                attack_name = attack_dict["name"]
                attack_freq = attack_dict["freq"]
                count = count + attack_freq
                if rand_num < count:
                    break
        # return attack['id']
        return self.get_attack(attack_name=attack_name)

    def choose_targets(self):
        pass

    def do_attack(self, target, attack: Attack) -> bool:
        """Perform an attack on a Toon, given an attack damage
        Args:
            target (Toon): Toon object that is going to be attacked
            attack (CogAttack): Attack's damage attack
        Returns:
            bool: False if the attack misses, True if it hits
        """
        if type(target) != BattleEntity:
            raise InvalidCogAttackTarget(
                f"{self}'s attack target ({target}) " "must be a Toon"
            )
        # #52, skip Cog attack if lured
        if self.is_lured:
            print(f"            [-] Cog `do_attack()` Skip lured {self}")
            return False

        # TODO #10, add chance_to_hit
        attack_hit = Entity.do_attack(self, target=target, attack=attack)
        return attack_hit
