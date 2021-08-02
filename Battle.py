from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from random import choice as rand_choice
from random import randint
from typing import List, Tuple

from .Attack import Attack
from .AttackGlobals import GROUP, MULTIPLIER, MULTIPLIER_DEFAULT
from .Cog import Cog
from .Entity import BattleEntity, Entity
from .Exceptions import (CogAlreadyTrappedError, CogLuredError, Error,
                         InvalidCogAttackTarget, TooManyCogsError,
                         TooManyToonsError)
from .Gag import Gag, get_gag_track_name
from .GagGlobals import TRACK
from .Toon import Toon

# TODO Create BattleCogBuilding w/ constructor accepting multi-toon&cogs
# TODO Look into Strategy design patterns for Toon decision making
# TODO #38 Different strategies: max_reward, fast_win_ignore_reward, survive..
# Pass: Clicking on PASS lets you skip your turn. Since Cogs will attack the
# Toon who has done him the most damage, you are less likely to be attacked
# if you choose Pass. This is a good strategy in a group battle if your Laff
# points are dangerously low.


@dataclass
class BattleCog(BattleEntity):

    entity: Cog

    # Initialize default values for all properties
    _entity: Entity = field(init=False, repr=False)
    _is_lured: bool = field(init=False, default=False)
    _is_trapped: bool = field(init=False, default=False)
    _trap: Tuple[BattleToon, ToonAttack] = field(init=False, default=(None, None))

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
        print(f"                [>] is_lured : {self.is_lured} ->  {new_is_lured} on {self}")
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
    def key(self) -> str:
        return self.entity.key

    @property
    def level(self) -> int:
        return self.entity.level

    @property
    def relative_level(self) -> int:
        return self.entity.relative_level

    @property
    def trap(self) -> Tuple[BattleToon, ToonAttack]:
        return self._trap

    @trap.setter
    def trap(self, toon_and_gag_trap: Tuple[BattleToon, ToonAttack]) -> None:
        assert isinstance(toon_and_gag_trap, tuple)
        assert len(toon_and_gag_trap) == 2

        toon = toon_and_gag_trap[0]
        gag_trap = toon_and_gag_trap[1]
        assert isinstance(toon, BattleToon)
        assert isinstance(gag_trap, ToonAttack)
        print(f"                [>] self.trap : {self.trap} -> {toon_and_gag_trap} on {self}")
        self._trap = toon_and_gag_trap

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
        # return attack['id']
        return self.get_attack(attack_name=attack_name)

    def choose_targets(self):
        pass

    def do_attack(self, target, attack: CogAttack) -> bool:
        """Perform an attack on a Toon, given an attack damage

        Args:
            target (Toon): Toon object that is going to be attacked
            attack (CogAttack): Attack's damage attack

        Returns:
            bool: False if the attack misses, True if it hits
        """
        if type(target) != BattleToon:
            raise InvalidCogAttackTarget(f"{self}'s attack target ({target}) "
                                         "must be a Toon")
        # #52, skip Cog attack if lured
        if self.is_lured:
            print(f"            [-] Cog `do_attack()` Skip lured {self}")
            return False

        # TODO #10, add chance_to_hit
        attack_hit = Entity.do_attack(self, target=target, attack=attack)
        return attack_hit

    """
        # # TODO (??) Create CogStates
        # _is_lured: bool = field(init=False, default=False)
        # _is_trapped: bool = field(init=False, default=False)
        # _trap: Tuple[Entity, Gag] = field(init=False, default=None)

        # def __post_init__(self):
        #     self.vitals = get_cog_vitals(cog_key=self.key,
        #                                 relative_level=self.relative_level)
        #     self.name = self.vitals['name']
        #     self.hp_max = self.vitals['hp']

        #     super().__init__(name=self.name, hp=self.hp_max)
        #     self.attacks = self.vitals['attacks']
        #     self.defense = self.vitals['def']
        #     self.level = self.vitals['level']

        # @property
        # def is_lured(self) -> bool:
        #     return self._is_lured

        # @is_lured.setter
        # def is_lured(self, new_is_lured: bool) -> None:
        #     assert type(new_is_lured) == bool
        #     print(f"                [>] is_lured : {self.is_lured} -> "
        #         f"{new_is_lured} on {self}")
        #     if new_is_lured and self.is_lured:
        #         raise CogLuredError("Can't Lure a Cog that's already Lured")
        #     self._is_lured = new_is_lured

        # @property
        # def is_trapped(self) -> bool:
        #     return self._is_trapped

        # @is_trapped.setter
        # def is_trapped(self, new_is_trapped: bool) -> None:
        #     assert type(new_is_trapped) == bool
        #     print(f"                [>] is_trapped : {self.is_trapped} -> "
        #         f"{new_is_trapped} on {self}")
        #     if new_is_trapped:
        #         # If two or more Trap gags are deployed in front of the same cog,
        #         # the gags will "cancel" each other out and will render a waste.
        #         if self.is_trapped:
        #             raise CogAlreadyTrappedError
        #         # ! Trap gags cannot be placed if a Cog is already lured
        #         if self.is_lured:
        #             raise CogLuredError
        #         self._is_trapped = True
        #     else:
        #         self._is_trapped = False
        #         print(f"                [>] self.trap : {(self.trap)} -> None on {self}")  # noqa
        #         self._trap = None

        # @property
        # # def trap(self) -> tuple[Toon, Gag]:
        # def trap(self) -> tuple:
        #     return self._trap

        # @trap.setter
        # def trap(self, toon_and_gag_trap) -> None:
        #     assert type(toon_and_gag_trap) == tuple
        #     assert len(toon_and_gag_trap) == 2

        #     from .Gag import Gag
        #     from .Toon import Toon

        #     toon = toon_and_gag_trap[0]
        #     gag_trap = toon_and_gag_trap[1]
        #     assert type(toon) == Toon
        #     assert type(gag_trap) == Gag
        #     print(f"                [>] self.trap : {(self.trap)} -> ({toon}, "
        #         f"{gag_trap}) on {self}")
        #     self._trap = (toon, gag_trap)

        # # TODO #40, `choose_target` method to choose a target when vs 2+ toons
        # # TODO #39, Need to write tests for this method
        # def choose_attack(self, attack_name: str = '') -> CogAttack:
        #     \"""Return Attack obj containing Cog attack information from
        #         self.attacks, a pseudo-random Attack is returned by default
        #         unless the `attack_name` argument is provided

        #     Args:
        #         attack_name (str, optional): Attack name as seen in COG_ATTACKS or
        #             the `get_cog_attacks_all_levels` function

        #         Example of valid input ::
        #             <'PoundKey'|'Shred'|'ClipOnTie'>  # Returns <0|1|2>

        #     Returns:
        #         int: Index of the Cog attack
        #    \"""
        #     if attack_name == '':
        #         rand_num = randint(0, 99)
        #         count = 0
        #         for attack_dict in self.attacks:
        #             attack_name = attack_dict['name']
        #             attack_freq = attack_dict['freq']
        #             count = count + attack_freq
        #             if rand_num < count:
        #                 break
        #     return self.get_attack(attack_name=attack_name)

        #     # return attack['id']

        # def do_attack(self, target, attack: CogAttack) -> bool:
        #    \"""Perform an attack on a Toon, given an attack damage

        #     Args:
        #         target (Toon): Toon object that is going to be attacked
        #         attack (CogAttack): Attack's damage attack

        #     Returns:
        #         bool: False if the attack misses, True if it hits
        #    \"""
        #     # Have to import Toon here due to circular import issue when importing
        #     # Toon at the top of the file
        #     from .Toon import Toon

        #     if type(target) != Toon:
        #         raise InvalidCogAttackTarget(f"{self}'s attack target ({target}) "
        #                                     "must be a Toon")
        #     # #52, skip Cog attack if lured
        #     if self.is_lured:
        #         print(f"            [-] Cog `do_attack()` Skip lured {self}")
        #         return False

        #     # TODO #10, add chance_to_hit
        #     attack_hit = Entity.do_attack(self, target=target, attack=attack)
        #     return attack_hit
    """
    pass


@dataclass
class BattleToon(BattleEntity):

    entity: Toon

    # Initialize default values for all properties
    _entity: Toon = field(init=False, repr=False)
    _reward_multiplier = MULTIPLIER_DEFAULT

    @property
    def entity(self) -> Toon:
        return self._entity

    @entity.setter
    def entity(self, new_entity: Toon) -> None:
        if not isinstance(new_entity, Toon):
            raise ValueError("BattleToon.entity must be of type Toon")
        self._entity = new_entity

    @property
    def available_gags(self) -> List[ToonAttack]:
        """Return a list of available Gags which can be used to attack a target"""
        return self.entity.gags.available_gags

    @staticmethod
    def _gag_is_possible(gag: Gag, target: BattleCog) -> bool:
        """Return True if the Gag can be used against the target, regardless if there's a reward

        Certain Gags cannot be used against BattleCogs. For example...
            - a Lure Gag cannot be used against a Lured Cog
                UNLESS, there are other non-Lured Cogs in the Battle
            - a Trap Gag cannot be used against a Lured/Trapped Cog
                UNLESS, there are other non-Trapped Cogs in the Battle
            - a Heal (Toon-Up) Gag cannot be used against a Cog

        Args:
            gag (Gag): Gag object from the BattleToon.entity.gags
            target (BattleCog): BattleCog object to be attacked

        Returns:
            bool: True if the Gag can be used against the target
        """
        impossible_rules = [
            gag.track == TRACK.HEAL,
            target.is_lured and gag.track == TRACK.LURE,
            target.is_lured and gag.track == TRACK.TRAP,
            target.is_trapped and gag.track == TRACK.TRAP,
        ]
        return any(impossible_rules) is False

    def _gag_is_viable(self, gag: Gag, target: BattleCog) -> bool:
        """Return True if the Gag is possible and provides a reward

        Viable Gags are possible to use against the target and provide a rewards because the
        level of the Gag is lower than the target.

        Args:
            gag (Gag): Gag object from the BattleToon.entity.gags
            target (BattleCog): BattleCog object to be attacked

        Returns:
            bool: True if the Gag can be used against the target and provides a reward
        """
        unviable_rules = [
            self._gag_is_possible(gag=gag, target=target) is False,
            gag.level >= target.level
        ]
        return any(unviable_rules) is False

    def get_possible_attacks(self, target: BattleCog) -> List[ToonAttack]:
        """Return a list of possible attacks against a BattleCog target, ignore EXP reward

        Trap Gags are not returned against a Lured/Trapped Cog.
        Lure Gags are not returned against a Lured Cog.

        Args:
            target (BattleCog): BattleCog to be attacked

        Returns:
            List[ToonAttack]: List of possible attacks againt target, ignores EXP reward
        """
        possible_attacks = []
        for gag in self.available_gags:
            if self._gag_is_possible(gag=gag, target=target):
                attack = ToonAttack(gag=gag, target_cog=target)
                possible_attacks.append(attack)

        return possible_attacks

    def get_viable_attacks(self, target: BattleCog) -> List[ToonAttack]:
        """Return a list of viable attacks against a BattleCog target, weigh EXP rewards

        Trap Gags are not returned against a Lured/Trapped Cog.
        Lure Gags are not returned against a Lured Cog.

        Args:
            target (BattleCog): BattleCog to be attacked

        Returns:
            List[ToonAttack]: List of viable attacks againt target, weigh EXP rewards
        """
        possible_attacks = self.get_possible_attacks(target=target)
        return [attack for attack in possible_attacks if attack.gag.level < target.level]

    def choose_attack(self):
        return super().choose_attack()

    def choose_targets(self):
        return super().choose_targets()

    def update_reward_multiplier(self):
        """Update the BattleToon's reward multiplier when Battle pushes a notification"""
        self._reward_multiplier = self.battle.get_multiplier()


@dataclass
class CogAttack(Attack):

    # TODO: Add freq as an attribute

    def __repr__(self) -> str:
        return str(self.__dict__)


@dataclass(init=False)
class ToonAttack(Attack):

    def __init__(self, gag: Gag, target_cog: BattleEntity):
        self.gag = gag
        self.target_cog = target_cog

        super().__init__(
            name=self.gag.name,
            damage=self.gag.damage,
            accuracy=self.gag.accuracy,
            group=self.gag.target
        )

        # Trap-specific attributes used for tracking EXP rewards
        self._is_attack = False
        self._is_setup = False

    @property
    def is_attack(self) -> bool:
        return self._is_attack

    @is_attack.setter
    def is_attack(self, new_is_attack: bool) -> None:
        assert isinstance(new_is_attack, bool)

        print(f"                [>] is_attack : {self.is_attack} -> {new_is_attack} on {self}")  # noqa
        self._is_attack = new_is_attack

    @property
    def is_setup(self) -> bool:
        return self._is_setup

    @is_setup.setter
    def is_setup(self, new_is_setup: bool) -> None:
        assert isinstance(new_is_setup, bool)
        print(f"                [>] is_setup : {self.is_setup} -> {new_is_setup} on {self}")  # noqa
        self._is_setup = new_is_setup


@dataclass
class RewardCalculator:

    building_floor: int = 1
    is_invasion: bool = False

    @property
    def base_reward(self) -> List[int]:
        return [1, 2, 3, 4, 5, 6, 7]

    @property
    def reward_table(self) -> List[int]:
        return [round(reward * self.get_multiplier()) for reward in self.base_reward]

    @property
    def multiplier_building(self) -> float:
        """Return the multipler value from being in a Cog Building"""
        return MULTIPLIER.get_building_multiplier_from_floor(floor=self.building_floor)

    @property
    def multiplier_invasion(self) -> float:
        """Return the multipler value from being in a Cog Building"""
        return MULTIPLIER.get_invasion_multiplier_from_bool(is_invasion=self.is_invasion)

    def get_multiplier(self) -> float:
        """Return the reward multiplier

        Returns:
            float: Value used to calculate a BattleToon's ToonAttack reward
        """
        return self.multiplier_building * self.multiplier_invasion

    def get_base_reward(self, attack: ToonAttack) -> int:
        """Return the base reward of a Gag

        Args:
            attack (ToonAttack): BattleToon Attack containing that Gag and target BattleCog

        Returns:
            int: Base reward of a ToonAttack
        """
        return self.base_reward[attack.gag.level]

    def calculate_reward(self, attack: ToonAttack) -> int:
        """Calculate the BattleToon's reward, given a ToonAttack

        Return -1 if the Gag's level exceeds the target BattleCog's level, meaning the Gag is
        possible, but not viable.
        Return ((gag.level + 1) * multiplier) if the Gag's level is lower than the target's level.

        Args:
            attack (ToonAttack): BattleToon Attack containing that Gag and target BattleCog

        Returns:
            int: Skill points awarded for successfully landing the ToonAttack
        """
        if attack.gag.level >= attack.target_cog.level:
            return -1
        # Round upwards because the reward could be x.5
        return self.reward_table[attack.gag.level]


# TODO class RewardTracker, remove `calculate_rewards` from Battle
# TODO Battle should only have addition of Cogs/Toons and updating the Battle
class Battle:

    # Countdown timer for the Toon[s] to select a Gag and Target, or escape
    # Cog[s] will attack if no Gag and Target is provided by the Toon[s]
    countdown_timer = 99

    def __init__(self, first_cog: BattleCog, first_toon: BattleToon,
                 building_floor: int = MULTIPLIER.FLOOR1, invasion: bool = False):
        self.reward_calculator = RewardCalculator(building_floor=building_floor, invasion=invasion)

        self.is_battling = True

        self._states = []
        self._toons = []

    @property
    def toons(self) -> list[BattleEntity]:
        return self._toons

    @toons.setter
    def toons(self, toons: list[BattleToon]) -> list[BattleToon]:
        if len(toons) > 4:
            raise TooManyToonsError
        assert all([type(x) == BattleToon for x in toons])
        self._toons = toons

    def add_toon(self, new_toon: BattleToon) -> None:
        assert type(new_toon) == BattleToon
        if len(self._toons) >= 4:
            print(f"    [!] ERROR : Too many Toons battling, can't add Toon "
                  f"{new_toon}")
            raise TooManyToonsError(new_toon)
        self.register(new_toon)

    def get_multiplier(self) -> float:
        return self.reward_calculator.get_multiplier()

    def notify(self):
        """Notify all observers of changes to RewardCalculator.multiplier"""
        for battle_toon in self.toons:
            battle_toon.update_reward_multiplier()

    def register(self, toon: BattleToon):
        """Register an observer Toon"""
        self._toons.append(toon)
        toon.update_reward_multiplier()  # Update the Toon's reward multiplier

    def unregister(self, toon: BattleToon):
        """Unregister an observer Toon"""
        self._toons.remove(toon)

    def update(self):
        self.update()
        if type(self.state) == EndState:
            self.is_battling = False


class BattleContext:

    def __init__(self, state: BattleState, cogs: list[BattleEntity], toons: list[BattleEntity],
                 rewards: dict[BattleEntity:dict[int:int]]) -> None:
        # ! Battle should always begin at ToonAttackState
        print("\n[^] Initializing BattleContext...")
        self.cogs = cogs
        self.toons = toons
        self.rewards = rewards

        self._completed_states = []

        self.state = state
        self.state.context = self

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def state(self) -> BattleState:
        return self._state

    @state.setter
    def state(self, new_state: BattleState) -> None:
        # print(f"        [>] Setting new state: {new_state}")
        self._state = new_state

    @property
    def cogs(self) -> list:
        return self._cogs

    @cogs.setter
    def cogs(self, cogs: list[BattleEntity]) -> None:
        if len(cogs) > 4:
            raise TooManyCogsError
        assert all([type(x) == BattleEntity for x in cogs])
        self._cogs = cogs

    @property
    def toons(self) -> list[BattleEntity]:
        return self._toons

    @toons.setter
    def toons(self, toons: list[BattleEntity]) -> list:
        if len(toons) > 4:
            raise TooManyToonsError
        assert all([type(x) == BattleEntity for x in toons])
        self._toons = toons

    def add_cog(self, new_cog: BattleEntity) -> None:
        assert type(new_cog) == BattleEntity
        if len(self._cogs) == 4:
            raise TooManyCogsError(new_cog)
        self._cogs.append(new_cog)

    def add_toon(self, new_toon: BattleEntity) -> None:
        assert type(new_toon) == BattleEntity
        if len(self._toons) == 4:
            raise TooManyToonsError(new_toon)
        self._toons.append(new_toon)

    def remove_cog(self, defeated_cog: BattleEntity) -> None:
        assert type(defeated_cog) == BattleEntity
        print(f"            [-] BattleEntity {defeated_cog} is defeated")
        self.cogs.remove(defeated_cog)

    def transition_to(self, new_state: BattleState):
        print(f"    [+] `transition_to()` transition : {self.state} -> {new_state}")  # noqa
        self._completed_states.append(self.state)
        self.state = new_state
        print(f"        [-] `transition_to()` completed states : {[str(state) for state in self._completed_states]}")  # noqa
        self.state.context = self

    def update(self):
        print(f"[+] {self} `update()` pre-update state : {self.state}")

        if issubclass(self.state.__class__, AttackState):
            print(f"    [+] `handle_attacks()` {self.state} ")
            self.state.handle_attacks()
        elif issubclass(self.state.__class__, WinLoseState):
            print(f"    [+] `handle_win_lose()` {self.state} ")
            self.state.handle_win_lose()
        elif type(self.state) == EndState:
            print(f"    [$] Do we want to do anything in {self.state}?")
            pass  # ? Do we want to do anything in EndState?
        else:
            raise TypeError(self.state)

        print(f"    [-] {self} `update()` post-update state : {self.state}")  # noqa


class BattleState(ABC):

    @property
    def context(self) -> BattleContext:
        return self._context

    @context.setter
    def context(self, context: BattleContext) -> None:
        self._context = context

    def __str__(self) -> str:
        return self.__class__.__name__


class AttackState(BattleState):

    @abstractmethod
    def handle_attacks():
        raise NotImplementedError

    def __init__(self):
        raise Exception("[!] ERROR: Entering state: AttackState")


class WinLoseState(BattleState):

    @abstractmethod
    def handle_win_lose():
        raise NotImplementedError

    def __init__(self):
        raise Exception("[!] ERROR: Entering state: WinLoseState")

    # TODO #37, #45: Implement methods to add rewards, level up BattleEntity


# Do we need a ToonChooseAttack state and ToonDoAttack state? Likely yes, will
# be easier to debug and tweak decision-making of the AI.
# Will also make it easier to implement Strategy design pattern
class ToonAttackState(AttackState):

    # ! ToonAtkState : If all Cogs defeated -> WinState else CogAtkState
    def __init__(self):
        self.attacks = []  # [(BattleEntity, BattleEntity, Gag, atk_hit_or_miss: int [0|1])]
        # Keep track of which Cogs are being targeted and by how many Toons
        self.overdefeat_cogs = {}
        # TODO #51, Add bonus EXP multipliers as a ToonAttackState property

    def handle_attacks(self):
        potential_attacks = {}
        self.overdefeat_cogs = {cog: {} for cog in self.context.cogs}

        # #44, Group and order attacks by Gag.track rather than sequential
        # Select Targets and choose Gag Attacks
        for toon in self.context.toons:
            if toon.is_defeated:
                continue
            # TODO #40, choose_target
            """
            1. Get viable attacks against all Cogs
            2. Randomly pick one viable attack Gags list to use
                2a. Must have at least 1 viable Gag in the list
                2b. If no viable Gags available for any target, we pass/stall
            3. Randomly pick one attack from the viable Gags list
            """
            alive_cogs = [
                cog for cog in self.context.cogs if not cog.is_defeated]

            target_cogs, gag_atk = toon.choose_attack(targets=alive_cogs)
            print(f"            [-] BattleEntity {toon} targets BattleEntity {target_cogs}")
            # #44, Group attacks by Gag.track
            if gag_atk.track not in potential_attacks:
                potential_attacks[gag_atk.track] = []

            # Track which Cogs are being targeted and by how many Toons
            for target_cog in target_cogs:
                if gag_atk.track not in self.overdefeat_cogs[target_cog]:
                    self.overdefeat_cogs[target_cog][gag_atk.track] = 0
                self.overdefeat_cogs[target_cog][gag_atk.track] += 1

            potential_attack = (toon, target_cogs, gag_atk)
            potential_attacks[gag_atk.track].append(potential_attack)

        # #44, Do attacks in order, sorted ascending (low->high) GagTrack index
        for gag_track in sorted(potential_attacks):
            # TODO #20, Calculate bonus damage
            # highest_accuracy = max(
            #     gag.accuracy for _, _, gag in potential_attacks[gag_track])
            # total_damage = sum(
            #     gag.damage for _, _, gag in potential_attacks[gag_track])

            print(f"        [>] Gag Track : {get_gag_track_name(gag_track)}")
            for toon, target_cogs, gag_atk in potential_attacks[gag_track]:
                # If 2+ Toons are attacking the same BattleEntity with the same GagTrack
                #   Set overdefeat to True to override CogAlreadyDefeatedError
                for cog in target_cogs:
                    is_overdefeat = self.overdefeat_cogs[cog][gag_atk.track] > 1  # noqa
                    # Cache cog.trap.. if BattleEntity uses Lure and the Trap activates
                    cog_is_trapped = cog.is_trapped
                    if cog_is_trapped:
                        trap_toon, trap_gag = cog.trap
                    # TODO #10, Add chance_to_hit
                    attack_hit = toon.do_attack(target=cog, gag_atk=gag_atk,
                                                overdefeat=is_overdefeat)
                    # Attack doesn't miss and Gag is eligible for reward
                    if attack_hit:
                        # Activate the Trap Gag if the BattleEntity lures a trapped BattleEntity
                        if cog.is_lured and cog_is_trapped:
                            self.attacks.append((trap_toon, cog, trap_gag,
                                                 attack_hit))

                self.attacks.append((toon, target_cogs, gag_atk, attack_hit))

            for cog in self.context.cogs:
                if cog.is_defeated:
                    self.context.remove_cog(defeated_cog=cog)

        if all([cog.is_defeated for cog in self.context.cogs]):
            # ! First need to check if all cogs defeated, then battle is Won
            transition_state = WinState
        else:
            transition_state = CogAttackState
        self.context.transition_to(new_state=transition_state())


class CogAttackState(AttackState):

    def __init__(self):
        self.attacks = {}  # {BattleEntity: (BattleEntity, Damage)}

    def handle_attacks(self):
        transition_state = ToonAttackState

        for cog in self.context.cogs:
            cog_atk = cog.manual_atk if cog.manual_atk is not None else cog.choose_attack()  # noqa

            viable_toons = [toon for toon in self.context.toons
                            if not toon.is_defeated]
            if cog_atk.target == GROUP.MULTI:
                print(f"        [+] {self} BattleEntity {cog} targets all Toons "
                      f"{viable_toons}")
                for toon in viable_toons:
                    atk_hit = cog.do_attack(target=toon, attack=cog_atk)
                    if toon.is_defeated:
                        print(f"            [-] BattleEntity {target_toon} is defeated")  # noqa
                        # ! If all Toons defeated -> LoseState else ToonAtkState  # noqa
                    self.attacks[cog] = (toon, cog_atk, atk_hit)

            else:
                # TODO #40, choose_target
                target_toon = rand_choice(viable_toons)
                print(f"        [+] {self} BattleEntity {cog} targets BattleEntity "
                      f"{target_toon}")
                atk_hit = cog.do_attack(target=target_toon, attack=cog_atk)
                self.attacks[cog] = (target_toon, cog_atk, atk_hit)

                if target_toon.is_defeated:
                    print(f"            [-] BattleEntity {target_toon} is defeated")
                    # ! If all Toons defeated -> LoseState else ToonAtkState

            if all([toon.is_defeated for toon in self.context.toons]):
                transition_state = LoseState
                break

        self.context.transition_to(new_state=transition_state())


class WinState(WinLoseState):

    # Need an __init__ function, otherwise it'll initialize as an WinLoseState
    def __init__(self):
        super()

    def handle_win_lose(self):
        """ # TODO #9, #37, #46
        * 1. If attack hits and all Cogs are defeated, calculate EXP and add to
        *    gag track EXP (AI reward)

        * 2. Add EXP multiplier (cog building, invasions)
        """
        print("        [-] TODO #9, #37, #46")
        # self.reward = self.calculate_rewards()
        # total_reward = sum(state.reward for state in self.reward)
        # print(f"[$] Total Reward = {total_reward}")

        if all([cog.is_defeated for cog in self.context.cogs]):
            transition_state = EndState
        else:
            raise Error("We should be in EndState")
        self.context.transition_to(new_state=transition_state())


class LoseState(WinLoseState):
    # TODO #37, #45: Implement methods to calculate rewards, remove BattleEntity's Gags
    # TODO #9, implement functionality & create tests for BattleEntity losing to BattleEntity

    # Need an __init__ function, otherwise it'll initialize as an WinLoseState
    def __init__(self):
        super()

    def handle_win_lose(self):
        # TODO #11, replace this double for-loop with Gag objects
        # TODO Alternatively, make BattleEntity.is_defeated a property, strip all the
        # Gags in the setter method if BattleEntity.is_defeated is True
        defeated_toons = [
            toon for toon in self.context._toons if toon.is_defeated]

        for toon in defeated_toons:
            print(f"        [-] Removing all Gags from BattleEntity {toon}")
            for track_idx, gag_track in enumerate(toon.gags):
                for gag_idx, gag in enumerate(toon.gags[track_idx]):
                    # Set the Gag count to 0 if the Gag is unlocked, or leave
                    # the Gag locked
                    toon.gags[track_idx][gag_idx] = 0 if gag != -1 else -1

        self.context.reward = [0] * 7
        self.context.transition_to(new_state=EndState())


class EndState(BattleState):
    pass
