from __future__ import annotations

from dataclasses import dataclass, field
from random import choice as rand_choice
from typing import List, Optional

from .Entity import Entity
from .Exceptions import (GagCountError, LockedGagError, LockedGagTrackError,
                         NotEnoughGagsError, TooManyGagsError)
from .Gag import (Gag, count_all_gags,  get_gag_exp, get_gag_exp_needed)
from .GagGlobals import TRACK, LEVELS

DEFAULT_HP = 15
# -1 means the gag_track is locked,0 means lvl 1 Gag is unlocked
DEFAULT_LEVELS = [-1, -1, -1, -1, 0, 0, -1]
# Populate DEFAULT_EXP from Gag track levels in DEFAULT_LEVELS
DEFAULT_EXPS = [LEVELS[idx][level] for idx, level in enumerate(DEFAULT_LEVELS)]
# DEFAULT_EXPS = [0, 0, 0, 0, 10, 10, 0]
DEFAULT_GAGS = [[-1, -1, -1, -1, -1, -1, -1],  # Toon-Up
                [-1, -1, -1, -1, -1, -1, -1],  # Trap
                [-1, -1, -1, -1, -1, -1, -1],  # Lure
                [-1, -1, -1, -1, -1, -1, -1],  # Sound
                [0,  -1, -1, -1, -1, -1, -1],  # Throw
                [0,  -1, -1, -1, -1, -1, -1],  # Squirt
                [-1, -1, -1, -1, -1, -1, -1]]  # Drop
DEFAULT_GAG_LIMIT = 20


@dataclass
class Toon(Entity):
    """Toon object class

    Args:
        name (str): Name of the Toon
        hp (int, optional): Laff-o-Meter (health points) of a Toon
        gags (list, optional): 2-D list, ex: `gags[GAG_TRACK][GAG]`.
            Defaults to DEFAULT_GAGS.
            Example `gags` ::
                gags = [[0,   0,  0,  5,  5,  3, -1],  # 0 Toon-up
                        [-1, -1, -1, -1, -1, -1, -1],  # 1 Trap (locked)
                        [0,   0,  0,  0,  5,  3,  1],  # 2 Lure
                        [0,   0,  0,  0,  5,  3, -1],  # 3 Sound
                        [0,   2,  1,  4,  4,  2, -1],  # 4 Throw
                        [0,   0,  0,  5,  5,  3, -1],  # 5 Squirt
                        [0,   9,  5, -1, -1, -1, -1]]  # 6 Drop

        gag_exps (list, optional): List containing Gag track EXP.
            Defaults to DEFAULT_EXPS.
            Example `gag_exps` ::
                gag_exps = [7421,   # 0 Toon-up
                            0,      # 1 Trap (locked)
                            10101,  # 2 Lure
                            9443,   # 3 Sound
                            8690,   # 4 Throw
                            6862,   # 5 Squirt
                            191]    # 6 Drop

        gag_levels (list, optional): List containing Gag track levels.
            Defaults to DEFAULT_LEVELS.
            Example `gag_levels` ::
                gag_levels = [5,   # 0 Toon-up
                                -1,  # 1 Trap (locked)
                                6,   # 2 Lure
                                5,   # 3 Sound
                                5,   # 4 Throw
                                5,   # 5 Squirt
                                2]   # 6 Drop

        gag_limit (int, optional): Maximum number of Gags a Toon can carry.
            Defaults to DEFAULT_GAG_LIMIT.
    """

    hp: Optional[int] = field(default=DEFAULT_HP)
    gags: Optional[List[List[int]]] = field(default_factory=list)
    gag_exps: Optional[List[int]] = field(default_factory=list)
    gag_levels: Optional[List[int]] = field(default_factory=list)
    gag_limit: Optional[int] = field(default=DEFAULT_GAG_LIMIT)

    def __post_init__(self):
        super().__init__(name=self.name, hp=self.hp)

        if self.gags == []:
            self.gags = DEFAULT_GAGS.copy()
        if self.gag_exps == []:
            self.gag_exps = DEFAULT_EXPS.copy()
        if self.gag_levels == []:
            self.gag_levels = DEFAULT_LEVELS.copy()
        self.hp_max = self.hp
        # Verify total Gag count in `gags` doesn't exceed `gag_limit`
        if self._count_all_gags() > self.gag_limit:
            self.gags = DEFAULT_GAGS.copy()

    def __str__(self):
        return f'"{self.name}" ({self.hp}/{self.hp_max}hp)'

    def __repr__(self):
        return self.__str__()

    def _count_all_gags(self) -> int:
        """Return the Toon's total number of usable Gags

        Returns:
            int: Total number of Gags
        """
        count = count_all_gags(gags=self.gags)

        if count > self.gag_limit:
            raise TooManyGagsError(count, self.gag_limit)
        if count < 0:
            raise GagCountError

        return count

    def _count_gag(self, track: int, level: int) -> int:
        """Return Toon's current quantity of a Gag(gag_track, gag_level)

        Args:
            gag_track (int): Index number of the Gag Track <0-6>
            gag_level (int): Level of the Gag <0-6>

        Returns:
            int: Current quantity of a Gag
        """
        assert track in range(7)
        assert level in range(7)

        count = self.gags[track][level]

        return count

    def _count_gag_track(self, track: int) -> int:
        """Return Toon's current number of Gags in a Gag track

        Args:
            gag_track (int): Index number of the Gag Track <0-6>

        Returns:
            int: Current quantity of a Gag track
        """
        count = sum(self.gags[track], start=self.gags[track].count(-1))
        return count

    def _get_gag(self, track: int, level: int) -> Gag:
        count = self._count_gag(track=track, level=level)
        # count_max =  # ! TODO #42
        exp = self.get_gag_exp(track=track)
        return Gag(track=track, exp=exp, level=level, count=count)

    def _has_gag(self, track: int, level: int) -> bool:
        """True if Toon has the Gag, False if Toon doesn't have, or hasn't yet
            unlocked, the Gag.

        Args:
            track (int): Index number of the Gag Track <0-6>
            level (int): Level of the Gag <0-6>

        Returns:
            bool: True if Toon has the Gag
        """
        # Not in [0, -1]
        return self._count_gag(track=track, level=level) > 0

    # ! TODO #38, this & all attack-related stuff should go into Strategy
    def _pick_random_gag(self, target=None, attack=False) -> Gag:
        if self._count_all_gags() == 0:
            # If there are no Gags at all, raise GagCountError and restock
            # TODO Need another error, this one is for individual Gags
            raise GagCountError

        gags = self.gags if target is None else self.get_viable_attacks(target=target)

        # Verify there's at least 1 viable Gag, given the Cog's level
        if target:
            # If no Gags are viable (e.g. gag.unlocked & gag.count>0), expand
            # the random Gag selection to all of the Toon's Gags
            if count_all_gags(gags=gags) == 0:
                print(f"        [!] WARNING `_pick_random_gag` : Toon {self} "
                      f"does not have any viable attacks against Cog {target}")
                print("            [-] Expanding random Gag selection to all "
                      "Gags")
                gags = self.gags

        # If there are no viable Gags at all, raise GagCountError and restock
        if count_all_gags(gags=gags) == 0:
            raise GagCountError

        # Example `viable_gags` = [(track, level), (track, level), ... ]
        # TODO : How can we utilize get_viable_gags here?
        # Can we just do [(track_index, gag_level) for track, level in gags if gag_count > 0]
        viable_gags = []
        for track_index, gag_track in enumerate(gags):
            for gag_level, gag_count in enumerate(gag_track):
                # TODO #38, add different rules for different Strategies
                # TODO #38, Create Rules for valid Gags using numpy masks,
                # validate against those Rules. We can make more custom
                # exceptions for this when we make strategies.

                rules = [gag_count not in [0, -1],
                         # Toons cannot use Heal as an attack
                         track_index != TRACK.HEAL if attack is True else 1
                         ]
                if target:
                    # Can't lure a lured Cog
                    rules.append(
                        track_index != TRACK.LURE if target.is_lured else 1)
                    # Can't trap a trapped Cog
                    rules.append(
                        track_index != TRACK.TRAP if target.is_trapped else 1)

                # If all rules pass, this Gag is viable
                if all(rules):
                    viable_gags.append((track_index, gag_level))

        if viable_gags == []:
            raise NotEnoughGagsError

        gag_track, gag_level = rand_choice(viable_gags)
        random_gag = self.choose_gag(track=gag_track, level=gag_level,
                                     attack=attack)
        return random_gag

    def _pick_random_attack(self, target) -> Gag:
        return self._pick_random_gag(target=target, attack=True)

    def choose_gag(self, track: int, level: int, attack=False) -> Gag:
        """Return Gag object containing Gag's vital info, iff Toon has the Gag

        Args:
            track (int): Index number of the Gag Track <0-6>
            level (int): Level of the Gag <0-6>
            attack (bool, optional) : True if called by `choose_attack()`.
                                      Defaults to False

        Returns:
            Gag: Vital information about the Toon's Gag
        """
        gag = self._get_gag(track=track, level=level)
        if gag.count == 0:
            raise NotEnoughGagsError(gag)
        if self.gags[track] == [-1]*7:
            raise LockedGagTrackError(track=track)
        if gag.count == -1:
            raise LockedGagError(level=level)

        gag_or_atk = 'gag' if not attack else 'attack'
        print(f"        [+] Toon `choose_{gag_or_atk}()` {self} : {gag}")
        return gag

    def get_gag_exp(self, track: int) -> int:
        """Get EXP for a Toon's Gag Track, given track# and list of exps

        Args:
            track (int): Index number of the Gag Track <0-6>

            Example of valid input ::
                0     # TRACK.HEAL
                1     # TRACK.TRAP
                2     # TRACK.LURE
                3     # TRACK.SOUND
                4     # TRACK.THROW
                5     # TRACK.SQUIRT
                6     # TRACK.DROP

        Returns:
            int: Toon's current Gag Track EXP
        """
        # return self.gag_exps[track]
        return get_gag_exp(track=track, current_exps=self.gag_exps)

    def get_gag_exp_needed(self, track: int) -> int:
        """Return the Gag Track EXP required to advance to next Gag Track level

        Args:
            track (int): Index number of the Gag Track <0-6>

            Example of valid input ::
                0     # TRACK.HEAL
                1     # TRACK.TRAP
                2     # TRACK.LURE
                3     # TRACK.SOUND
                4     # TRACK.THROW
                5     # TRACK.SQUIRT
                6     # TRACK.DROP

        Returns:
            int: EXP required to level up the Toon's Gag Track
        """
        return get_gag_exp_needed(track=track,
                                  current_exps=self.get_gag_exp(track)
                                  )

    # TODO #38, We should move this to Strategy, when we make Strategies.
    # TODO #38, Make sure to check against the highest level Cog in the battle
    # However, if the Cog being attacked is at a lower level than the gag,
    # then the toon will receive no skill points.
    # https://toontown.fandom.com/wiki/Skill_points#Earning_skill_points

    def has_gags(self) -> bool:
        """True if Toon has any available Gags, checks quantity of all Gags

        Returns:
            bool: True if Toon has any available Gags
        """
        # [[0]*7]*7 == 2-D list, 7x7, initialized with 0's
        # Return True if the 2-D list is NOT empty, aka Toon has Gags
        # return self.gags != [[0]*7]*7
        return self._count_all_gags() != 0
