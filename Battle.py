from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from random import choice as rand_choice
from random import randint
from typing import List, Tuple, Union

from .Attack import Attack
from .AttackGlobals import GROUP
from .Cog import Cog
from .Entity import BattleEntity, Entity
from .Exceptions import (CogAlreadyTrappedError, CogLuredError, Error,
                         InvalidCogAttackTarget, TooManyCogsError,
                         TooManyGagsError, TooManyToonsError)
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
        return self.cog.key

    @property
    def level(self) -> int:
        return self.cog.level

    @property
    def relative_level(self) -> int:
        return self.cog.relative_level

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

    @property
    def entity(self) -> Toon:
        return self._entity

    @entity.setter
    def entity(self, new_entity: Toon) -> None:
        if not isinstance(new_entity, Toon):
            raise ValueError("BattleToon.entity must be of type Toon")
        self._entity = new_entity

    def get_possible_attacks(self, target: BattleCog) -> List[Gag]:
        """Return a list of possible attacks against a BattleCog target, ignore EXP reward

        Trap Gags are not returned against a Trapped Cog.
        Lure Gags are not returned against a Lured Cog.

        Args:
            target (BattleCog): BattleCog to be attacked

        Returns:
            List[Gag]: List of possible attacks againt target, ignores EXP reward
        """
        pass

    def get_viable_attacks(self, target: BattleCog) -> List[Gag]:
        """Return a list of viable attacks against a BattleCog target, weigh EXP rewards

        Trap Gags are not returned against a Trapped Cog.
        Lure Gags are not returned against a Lured Cog.

        Args:
            target (BattleCog): BattleCog to be attacked

        Returns:
            List[Gag]: List of viable attacks againt target, weigh EXP rewards
        """
        pass

    def choose_attack(self):
        return super().choose_attack()

    def choose_targets(self):
        return super().choose_targets()


@dataclass
class CogAttack(Attack):

    # TODO: Add freq as an attribute

    def __repr__(self) -> str:
        return str(self.__dict__)


@dataclass(init=False)
class ToonAttack(Attack):

    def __init__(self, gag: Gag, target_cogs: Union[BattleEntity, List[BattleEntity]]):
        self.gag = gag
        super().__init__(
            name=self.gag.name,
            damage=self.gag.damage,
            accuracy=self.gag.accuracy,
            target=self.gag.target
        )

        self.target_cogs = target_cogs
        if isinstance(self.target_cogs, BattleCog):
            self.target_cogs = [self.target_cogs]

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


# TODO class RewardTracker, remove `calculate_rewards` from Battle
# TODO Battle should only have addition of Cogs/Toons and updating the Battle
class Battle:

    # Countdown timer for the Toon[s] to select a Gag and Target, or escape
    # Cog[s] will attack if no Gag and Target is provided by the Toon[s]
    countdown_timer = 99

    def __init__(self, first_cog: BattleCog, first_toon: BattleToon):
        # self._reward = [0]*7
        self._rewards = {first_toon: [0]*7}
        self._states = []
        self._context = BattleContext(state=ToonAttackState(),
                                      cogs=[first_cog],
                                      toons=[first_toon],
                                      rewards=self._rewards)
        self.is_battling = True

    @property
    def context(self):
        return self._context

    @property
    def cogs(self):
        return self.context.cogs

    @property
    def toons(self):
        return self.context.toons

    # TODO #49, Create negative test for adding new Toon/Cog
    def add_cog(self, new_cog: BattleCog):
        try:
            self.context.add_cog(new_cog)
        except TooManyGagsError as e:
            print(f"[!] ERROR : Cannot add Cog {new_cog}, too many Cogs")
            raise e

    def add_toon(self, new_toon: BattleToon):
        try:
            self.context.add_toon(new_toon)
            self._rewards[new_toon] = [0]*7
        except TooManyToonsError as e:
            print(f"    [!] ERROR : Too many Toons battling, can't add Toon "
                  f"{new_toon}")
            raise e

    def calculate_rewards(self) -> list:
        # import pprint  # To make rewards output readable
        # pp = pprint.PrettyPrinter(indent=1)
        print("[$] `calculate_rewards()` for all Toons")
        toon_attack_states = [
            state for state in self.context._completed_states if
            type(state) == ToonAttackState
        ]

        for attack_state in toon_attack_states:
            for toon, cogs, gag, atk_hit in attack_state.attacks:
                # TODO #51, Multiply reward by EXP multiplier
                if atk_hit:
                    eligible = any([cog for cog in cogs if cog.level >= gag.level])
                    reward = gag.level + 1 if eligible else 0
                    if gag.track == TRACK.TRAP:  # Don't reward for Trap setup
                        reward = reward if gag.is_attack else 0
                else:  # Attack missed
                    reward = 0
                self._rewards[toon][gag.track] += reward
                print(f"    [>] {toon} {'+' if atk_hit else ''}{reward} {gag.track_name} exp ({gag}) against {cogs}")  # noqa

        # Sum rewards for all Toons
        for toon in self.toons:
            print(f"    [+] `calculate_rewards()` for Toon {toon}")
            # If Toon is defeated, no rewards are given
            if toon.is_defeated:
                self._rewards[toon] = [0]*7
                continue
            print(f"        [-] Total rewards for Toon {toon} : "
                  f"{self._rewards[toon]}")
        print("    [-] `calculate_rewards()` all rewards ... ")
        # pp.pprint(self._rewards)
        return self._rewards

    def update(self):
        self.context.update()
        if type(self.context.state) == EndState:
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

        self.context.reward = [0]*7
        self.context.transition_to(new_state=EndState())


class EndState(BattleState):
    pass
