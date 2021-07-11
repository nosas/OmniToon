from __future__ import annotations

from dataclasses import dataclass, field
from random import randint
from typing import Tuple

from .Attack import Attack, CogAttack, ToonAttack
from .BattleState import BattleContext, EndState, ToonAttackState
from .Cog import Cog
from .Entity import Entity
from .Exceptions import (CogAlreadyTrappedError, CogLuredError,
                         InvalidCogAttackTarget, InvalidTargetError,
                         TargetDefeatedError, TooManyGagsError,
                         TooManyToonsError)
from .GagGlobals import TRAP_TRACK
from .Toon import Toon

# from .Toon import DEFAULT_HP

# TODO Create BattleCogBuilding w/ constructor accepting multi-toon&cogs
# TODO Look into Strategy design patterns for Toon decision making
# TODO #38 Different strategies: max_reward, fast_win_ignore_reward, survive..
# Pass: Clicking on PASS lets you skip your turn. Since Cogs will attack the
# Toon who has done him the most damage, you are less likely to be attacked
# if you choose Pass. This is a good strategy in a group battle if your Laff
# points are dangerously low.


@dataclass
class BattleEntity(Entity):
    battle_id: int

    # TODO id: int = field(default=0)
    _attack: Attack = field(init=False, default=None)
    _target: BattleEntity = field(init=False, default=None)

    def __hash__(self) -> int:
        return hash((self.hp, self.name, self.battle_id))

    def _get_attacked(self, amount: int):
        self.hp -= amount

    def _get_healed(self, amount: int):
        self.hp += amount

    def do_attack(self, target: BattleEntity, attack: Attack,
                  overdefeat: bool = False, force_miss: bool = False) -> bool:
        if not isinstance(target, BattleEntity):
            raise InvalidTargetError("Target must be a subclass of BattleEntity")
        if type(target) == type(self):
            raise InvalidTargetError("Target must not be of the same type")

        if target.is_defeated and overdefeat is False:
            # Multiple Toons attack the same Cog with the same Gag track
            raise TargetDefeatedError(f"Cannot attack defeated {type(target)}")

        target_hp_before = target.get_hp()

        # TODO #10, Add chance_to_hit
        attack_hit = False if force_miss else True
        hit_miss = 'misses'
        damage = 0
        if attack_hit:
            hit_miss = 'hits'
            damage = attack.damage
        target._get_attacked(amount=damage)

        class_name = self.__class__.__name__
        # TODO Add attack name and object name
        print(f"            [-] {class_name} `do_attack()` {self} "
              f"{attack.name} {hit_miss} {target} -> {target_hp_before}hp-"
              f"{damage}dmg")
        return attack_hit


@dataclass
class BattleCog(Cog, BattleEntity):

    # # For testing purposes. See `test_cog_attack_damages_multiple_toons`
    manual_atk: CogAttack = field(init=False, default=None)
    _is_lured: bool = field(init=False, default=False)
    _is_trapped: bool = field(init=False, default=False)
    _trap: Tuple[BattleToon, ToonAttack] = field(init=False, default=None)

    def __post_init__(self):
        return super().__post_init__()

    def _clear_trap(self) -> None:
        self._trap = None

    @property
    def is_lured(self) -> bool:
        return self._is_lured

    @is_lured.setter
    def is_lured(self, new_is_lured: bool) -> None:
        assert isinstance(new_is_lured,  bool)
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
        assert isinstance(new_is_trapped,  bool)
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


@dataclass
class BattleToon(Toon, BattleEntity):

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
