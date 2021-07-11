from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from random import choice as rand_choice
from random import randint
from typing import List, Tuple, Union

from .Attack import Attack
from .AttackGlobals import ATK_TGT_MULTI
from .Cog import Cog
from .Entity import BattleEntity, Entity
from .Exceptions import (CogAlreadyTrappedError, CogLuredError, Error,
                         InvalidCogAttackTarget, TooManyCogsError,
                         TooManyGagsError, TooManyToonsError)
from .Gag import Gag, get_gag_track_name
from .GagGlobals import TRAP_TRACK
from .Toon import Toon

# TODO Create BattleCogBuilding w/ constructor accepting multi-toon&cogs
# TODO Look into Strategy design patterns for Toon decision making
# TODO #38 Different strategies: max_reward, fast_win_ignore_reward, survive..
# Pass: Clicking on PASS lets you skip your turn. Since Cogs will attack the
# Toon who has done him the most damage, you are less likely to be attacked
# if you choose Pass. This is a good strategy in a group battle if your Laff
# points are dangerously low.


@dataclass(init=False)
class BattleCog(Cog, BattleEntity):

    manual_atk: CogAttack = field(init=False, default=None)
    _is_lured: bool = field(init=False, default=False)
    _is_trapped: bool = field(init=False, default=False)
    _trap: Tuple[BattleToon, ToonAttack] = field(init=False, default=(None, None))

    def __init__(self, battle_id: int, key: str, relative_level: int = 0):
        self.battle_id = battle_id
        super().__init__(key=key, relative_level=relative_level)

    def _clear_trap(self) -> None:
        self._trap = None

    @property
    def is_lured(self) -> bool:
        return self._is_lured

    @is_lured.setter
    def is_lured(self, new_is_lured: bool) -> None:
        if not isinstance(new_is_lured, bool):
            raise TypeError

        if new_is_lured and self.is_lured:
            raise CogLuredError("Can't Lure a Cog that's already Lured")
        print(f"                [>] is_lured : {self.is_lured} -> "
              f"{new_is_lured} on {self}")
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


@dataclass(init=False)
class BattleToon(Toon, BattleEntity):
    def __init__(self):
        pass

    """
        #     name: str
        #     hp: Optional[int] = field(default=DEFAULT_HP)
        #     gags: Optional[List[List[int]]] = field(default_factory=list)
        #     gag_exps: Optional[List[int]] = field(default_factory=list)
        #     gag_levels: Optional[List[int]] = field(default_factory=list)
        #     gag_limit: Optional[int] = field(default=DEFAULT_GAG_LIMIT)

        #     def __post_init__(self):
        #         super().__init__(name=self.name, hp=self.hp)

        #         if self.gags == []:
        #             self.gags = DEFAULT_GAGS.copy()
        #         if self.gag_exps == []:
        #             self.gag_exps = DEFAULT_EXPS.copy()
        #         if self.gag_levels == []:
        #             self.gag_levels = DEFAULT_LEVELS.copy()
        #         self.hp_max = self.hp
        #         # Verify total Gag count in `gags` doesn't exceed `gag_limit`
        #         if self._count_all_gags() > self.gag_limit:
        #             self.gags = DEFAULT_GAGS.copy()

        # def choose_attack(self, targets: list[BattleCog], track: int = -1, level: int = -1,
        #                   ignore_level: bool = False) -> tuple[list[BattleCog], Gag]:
        #     \"""Return target Cog(s) and Gag object containing Gag's vital info

        #     Args:
        #         targets (list, optional): List of targetable Cogs, for choosing viable Gags
        #         track (int, optional): Index number of the Gag Track <0-6>
        #         level (int, optional): Level of the Gag <0-6>
        #         ignore_level (bool) : Mark Gags as viable despite being a higher lvl
        #             than the Cog. Defaults to False.

        #     Returns:
        #         Tuple(list[Cog], Gag): Target Cog(s) and vital info about Toon's Gag
        #     \"""
        #     # Get all viable attacks against all target Cogs
        #     all_viable_atks = {
        #         target: self.get_viable_attacks(target=target, ignore_level=ignore_level)
        #         for target in targets
        #         }

        #     # Verify there's at least 1 viable Gag in each viable_atk list
        #     for cog, viable_atks in all_viable_atks.items():
        #         # If there are no viable attacks, expand Gag selection to all Gags
        #         if count_all_gags(gags=viable_atks) == 0:
        #             atks = self.get_viable_attacks(target=cog, ignore_level=True)
        #             all_viable_atks[cog] = atks
        #             # There are no viable attacks for this target, delete the target
        #             if count_all_gags(gags=atks) == 0:
        #                 all_viable_atks[cog] = []

        #     # There are no viable attacks at all, pass/stall for time
        #     if all([atks == [] for atks in all_viable_atks.values()]):
        #         raise NotEnoughGagsError

        #     # Pick a random target Cog
        #     target_cog = rand_choice(list(all_viable_atks.keys()))
        #     # Create a list of possible attacks as tuples: [(gag_track, gag_level)]
        #     possible_attacks = []
        #     for track_index, gag_track in enumerate(all_viable_atks[target_cog]):
        #         for gag_level, gag_count in enumerate(gag_track):
        #             if gag_count > 0:
        #                 possible_attacks.append((track_index, gag_level))

        #     # If no arguments were provided, pick a random attack
        #     # If the desired Gag is not a valid possible attack, pick a rand attack
        #     if track == -1 and level == -1 or (track, level) not in possible_attacks:
        #         track, level = rand_choice(possible_attacks)
        #     gag_atk = self.choose_gag(track=track, level=level, attack=True)

        #     # Trap-specific attack logic:
        #     #   If the Cog is NOT Lured, set the Trap's setup attr to True so
        #     #   the Toon sets up the Trap rather than damages the Cog with the Trap
        #     if gag_atk.track == TRAP_TRACK:
        #         # No damage is done to Cog until the Cog is Lured onto the Trap
        #         # We're only setting up the Trap Gag here
        #         gag_atk.is_setup = True

        #     # Adjust target_cogs to include all Cogs if atk is multi-targeted
        #     target_cog = targets if gag_atk.target == ATK_TGT_MULTI else [target_cog]

        #     return (target_cog, gag_atk)

        # # TODO #11, Replace all gag_track,gag_level args to Gag objects
        # def do_attack(self, target: BattleCog, gag_atk: Gag, overdefeat=False) -> bool:
        #     \"""Perform an attack on a Cog, given a Gag

        #     Args:
        #         target (Cog): Cog object that is going to be attacked
        #         gag_atk (Gag): Gag object to be used for attacking
        #             * NOTE : There's specific attack logic for Lure/Trap/Drop
        #         overdefeat (bool, optional): Should be True if multiple Toons
        #                                      attack the same Cog with Gags of the
        #                                      same GagTrack. Defaults to False

        #     # TODO #53, Implement specific returns, e.g. Missed/Skipped/Hit
        #     Returns:
        #         bool: False if the attack misses, True if it hits
        #     \"""
        #     if type(target) != BattleCog:
        #         raise InvalidToonAttackTarget(f"{self}'s attack target ({target}) "
        #                                       "must be a Cog")
        #     attack_hit = False
        #     force_miss = False

        #     try:
        #         # TODO #10, Pass in attack_accuracy
        #         # ! If any(target==Trapped), acc of Lure gags increase by 20-30%
        #         # Trap-specific attack logic:
        #         #   If setting up Trap, don't do any damage to Cog
        #         #   If not setting up or attacking, we're attacking a Lured Cog
        #         #       and we should force a miss
        #         if gag_atk.track == TRAP_TRACK:
        #             if gag_atk.is_setup:
        #                 # No damage is done to Cog until the Cog is Lured onto Trap
        #                 gag_setup = Gag(track=gag_atk.track, exp=gag_atk.exp,
        #                                 level=gag_atk.level, count=gag_atk.count)
        #                 gag_setup.damage = 0
        #             elif not gag_atk.is_setup and not gag_atk.is_attack:
        #                 # ! This should only happen when using Trap on a Lured Cog
        #                 force_miss = True
        #                 if target.is_trapped:
        #                     target.is_trapped = False

        #         # Drop-specific attack logic:
        #         #   Force the Drop attack to miss if a Cog is Lured
        #         elif gag_atk.track == DROP_TRACK and target.is_lured:
        #             # Can't use Drop on a Lured Cog
        #             force_miss = True

        #         # ! Raises TargetDefeatedError if Cog is defeated
        #         attack = gag_atk if not gag_atk.is_setup else gag_setup

        #         attack_hit = Entity.do_attack(
        #             self, target=target, attack=attack, overdefeat=overdefeat,
        #             force_miss=force_miss)

        #         if attack_hit:
        #             # Lure-specific attack logic:
        #             #   Set Cog's is_lured attrs
        #             #   Activate Trap is a Cog.is_trapped
        #             if gag_atk.track == LURE_TRACK:
        #                 # ! Raises CogLuredError if Cog is already Lured
        #                 target.is_lured = True
        #                 # Activate the Trap & damage Cog if cog.is_trapped is True
        #                 if target.is_trapped:
        #                     trap_toon, trap_gag = target.trap
        #                     trap_gag.is_attack = True
        #                     # TODO #10, Add chance to hit == 100
        #                     trap_toon.do_attack(target=target, gag_atk=trap_gag)

        #             # Trap-specific attack logic:
        #             #   Set Cog's is_lured/trapped/trap attrs
        #             elif gag_atk.track == TRAP_TRACK:
        #                 # Trap should never be both is_attack and is_setup
        #                 assert not (gag_atk.is_attack and gag_atk.is_setup)

        #                 # if target.is_lured is True and target.is_trapped is True:
        #                 if gag_atk.is_attack is True:
        #                     target.is_lured = False
        #                     target.is_trapped = False
        #                     # ! Don't decrease Gag count bc we're activating the
        #                     # ! Trap, not setting it up
        #                     self.gags[gag_atk.track][gag_atk.level] += 1

        #                 # Set up the Trap Gag. Cog must be Lured to activate Trap
        #                 elif gag_atk.is_setup is True:
        #                     # ! Raises CogLuredError is Cog is already Lured
        #                     # ! Raises CogTrappedError is Cog already Trapped
        #                     target.is_trapped = True
        #                     gag_atk.is_setup = False
        #                     target.trap = (self, gag_atk)

        #             # Remove Cog's lured state when attacked by any Gag
        #             elif target.is_lured:
        #                 # TODO #20, add bonus damage for attacking lured Cog
        #                 target.is_lured = False

        #     except TargetDefeatedError:
        #         # Target is already defeated:
        #         #   Skip attack
        #         #   Increase Gag quantity by 1 to negate the -1 in `finally` block
        #         #   Return missed atk
        #         print(f"    [!] WARNING `do_attack()` : {self} tried to attack a "
        #               f"defeated Cog {target}")
        #         print(f"        [-] Skipping {gag_atk} attack, Cog {target} is "
        #               "already defeated")
        #         self.gags[gag_atk.track][gag_atk.level] += 1
        #         return False
        #     except CogLuredError:
        #         # Multiple Toons attack the same Cog with the same Gag track
        #         #   Overdefeat in case Lure activates a Trap and defeats the Cog
        #         #   so we still reward all Toons who Lured
        #         if gag_atk.track == LURE_TRACK:
        #             if overdefeat is True or gag_atk.target == ATK_TGT_MULTI:
        #                 return True
        #         lure_or_trap = "lure" if gag_atk.track == LURE_TRACK else "trap"
        #         print(f"    [!] WARNING `do_attack()` : {self} tried to "
        #               f"{lure_or_trap} a lured Cog {target}")
        #         return False
        #     except CogAlreadyTrappedError:
        #         print(f"    [!] WARNING `do_attack()` : {self} tried to "
        #               f"trap a trapped Cog {target}")
        #         print(f"        [-] Cancel existing Trap on Cog {target}: "
        #               f"({target.trap})")
        #         target.is_trapped = False
        #         return False
        #     except Exception as e:
        #         raise e

        #     finally:
        #         # ! Only reduce one if gag_atk.target == Multi
        #         self.gags[gag_atk.track][gag_atk.level] -= 1
        #         # TODO #37, Add Gag EXP (reward), so we can track rewards
        #         return attack_hit

        # def get_attack_accuracy(self, gag: Gag, target: BattleCog, bonus: int = 0) -> int:  # noqa
        #     \"""Calculate Gag Attack accuracy, given a Gag, Cog target, and
        #         optional bonus accuracy from Lures/Traps

        #     attack_accuracy = gag_accuracy + gag_exp + target_defense + bonus
        #         Source: https://toontownrewritten.fandom.com/wiki/Accuracy#propAcc

        #     Args:
        #         gag (Gag): Gag object obtained from `self.choose_attack()`
        #         target (Cog): Cog object that is going to be attacked
        #         bonus (int, optional): Bonus added when near a prop bonus during
        #                                Battle. Defaults to 0.

        #     Returns:
        #         int: Attack accuracy value in range <0-95>
        #     \"""
        #     # ! When Trap gag is used, atkAcc is set to 100, and atkHit is set to 1
        #     if gag.track == LURE_TRACK:
        #         return 100
        #     # ! For all other gags, if atkAcc exceeds 95, it will be reduced to 95
        #     gag_acc = get_gag_accuracy(track=gag.track, level=gag.level)
        #     gag_exp = self.get_gag_exp(track=gag.track)
        #     target_def = target.defense

        #     # ? Won't this always be 95 bc track_exp is easily > 95
        #     # ! Nope! We're calculating accuracy wrong. It shouldn't be track EXP
        #     atk_acc = gag_acc + gag_exp + target_def + bonus
        #     return min(atk_acc, 95)

        # def get_viable_attacks(self, target: BattleCog, ignore_level: int = False) -> list:
        #     \"""Return 2-D list of Gags that can be used and gain Gag EXP (reward)
        #         A Gag is viable if its level is below the Cog's level.

        #         NOTE: We're using 0-indexing for Gag levels, but 1-indexing for Cog

        #     Args:
        #         target (Cog): Cog object that is going to be attacked
        #         ignore_level (bool) : Mark Gags as viable despite being a higher lvl
        #             than the Cog. Defaults to False.

        #     Returns:
        #         list: 2-D list of Gags. 0 means the Gag is not available or
        #               does not gain Gag EXP when used. If all Gags are unviable,
        #               it will return the a list of the Toon's Gags.

        #     Example of Toon Astro's viable Gags against level 4 Cog ::
        #         input = toon_astro.gags = [
        #             [0,   0,  0,  5,  5,  3, -1],
        #             [-1, -1, -1, -1, -1, -1, -1],
        #             [0,   0,  0,  0,  5,  3,  1],
        #             [0,   0,  0,  0,  5,  3, -1],
        #             [0,   2,  1,  4,  4,  2, -1],
        #             [0,   0,  0,  5,  5,  3, -1],
        #             [0,   9,  5, -1, -1, -1, -1]
        #         ]

        #         output = all_viable_gags = [
        #             # ignore_level=False           # ignore_level=True
        #             [-1, -1, -1, -1, -1, -1, -1],  [-1, -1, -1, -1, -1, -1, -1],
        #             [-1, -1, -1, -1, -1, -1, -1],  [-1, -1, -1, -1, -1, -1, -1],
        #             [-1, -1, -1, -1, -1, -1, -1],  [-1, -1, -1, -1,  5,  3,  1],
        #             [-1, -1, -1, -1, -1, -1, -1],  [-1, -1, -1, -1,  5,  3, -1],
        #             [-1,  2,  1,  4, -1, -1, -1],  [-1,  2,  1,  4,  4,  2, -1],
        #             [-1, -1, -1,  5, -1, -1, -1],  [-1, -1, -1,  5,  5,  3, -1],
        #             [-1,  9,  5, -1, -1, -1, -1]   [-1,  9,  5, -1, -1, -1, -1]
        #         ]

        #     \"""
        #     all_viable_gags = self.get_viable_gags(target=target,
        #                                            ignore_level=ignore_level)
        #     all_viable_gags[HEAL_TRACK] = [-1]*7
        #     return all_viable_gags

        # def get_viable_gags(self, target: BattleCog, ignore_level: bool,
        #                     gags: list[list[int]] = None) -> list[list[int]]:
        #     \"""Return 2-D list of Gags that can be used and gain Gag EXP (reward)
        #         A Gag is viable if its level below the Cog's level.

        #     Args:
        #         target (Cog): Cog object that is going to be attacked
        #         ignore_level (bool) : Mark Gags as viable despite being a higher lvl
        #             than the Cog.
        #         gags (list, optional) : List of Gags

        #     Returns:
        #         list: 2-D list of Gags. 0 means the Gag is not available or
        #               does not gain Gag EXP when used. If all Gags are unviable,
        #               it will return the a list of the Toon's Gags.

        #     Example of Toon Astro's viable Gags against level 4 Cog ::
        #         input = toon_astro.gags = [
        #             [0,   0,  0,  5,  5,  3, -1],
        #             [-1, -1, -1, -1, -1, -1, -1],
        #             [0,   0,  0,  0,  5,  3,  1],
        #             [0,   0,  0,  0,  5,  3, -1],
        #             [0,   2,  1,  4,  4,  2, -1],
        #             [0,   0,  0,  5,  5,  3, -1],
        #             [0,   9,  5, -1, -1, -1, -1]
        #         ]

        #         output = all_viable_gags = [
        #             # ignore_level=False           # ignore_level=True
        #             [-1, -1, -1,  5, -1, -1, -1],  [-1, -1, -1,  5,  5,  3, -1],
        #             [-1, -1, -1, -1, -1, -1, -1],  [-1, -1, -1, -1, -1, -1, -1],
        #             [-1, -1, -1, -1, -1, -1, -1],  [-1, -1, -1, -1,  5,  3,  1],
        #             [-1, -1, -1, -1, -1, -1, -1],  [-1, -1, -1, -1,  5,  3, -1],
        #             [-1,  2,  1,  4, -1, -1, -1],  [-1,  2,  1,  4,  4,  2, -1],
        #             [-1, -1, -1,  5, -1, -1, -1],  [-1, -1, -1,  5,  5,  3, -1],
        #             [-1,  9,  5, -1, -1, -1, -1]   [-1,  9,  5, -1, -1, -1, -1]
        #         ]

        #     \"""
        #     # TODO  #11, Add Gag attributes to determine if valid/invalid/locked
        #     all_viable_gags = []

        #     for track_index, gag_track in enumerate(self.gags):
        #         viable_gags = gag_track.copy()

        #         # Impossible rules : Rules that can never be broken
        #         # Can't use Lure against a lured Cog
        #         # Can't use Trap against a lured/trapped Cog (fixes #71)
        #         # Drop could be viable if a Cog is lured, because another Toon can
        #         # attack the Cog when it's lured, and then we use Drop. But we'll
        #         # assume it's unviable until we develop Strategies
        #         # TODO #38
        #         if any([target.is_lured and track_index in [TRAP_TRACK, LURE_TRACK, DROP_TRACK],
        #                 target.is_trapped and track_index == TRAP_TRACK]
        #                ):
        #             all_viable_gags.append([-1]*7)
        #             continue

        #         # Compare each Gag. Unviable if count == 0 or Cog.level < gag.level
        #         for gag_level, gag_count in enumerate(viable_gags):
        #             # Can't use Gag if locked or quantity is 0
        #             if gag_count in [0, -1]:
        #                 viable_gags[gag_level] = -1
        #             # No reward if Gag lvl is greater than, or equal to, Cog lvl
        #             elif gag_level >= target.level:
        #                 viable_gags[gag_level] = gag_count if ignore_level else -1

        #         all_viable_gags.append(viable_gags)

        #     return all_viable_gags
    """
    pass


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
                    if gag.track == TRAP_TRACK:  # Don't reward for Trap setup
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
            highest_accuracy = max(
                gag.accuracy for _, _, gag in potential_attacks[gag_track])
            total_damage = sum(
                gag.damage for _, _, gag in potential_attacks[gag_track])

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
            if cog_atk.target == ATK_TGT_MULTI:
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
