from __future__ import annotations

from builtins import Exception

from .Gag import Gag


class Error(Exception):
    pass


class CountError(Error):
    pass


class TooManyCogsError(CountError):
    pass


class TooManyToonsError(CountError):
    pass


class GagCountError(CountError):
    pass


class LockedGagError(GagCountError):
    """ Toon has not unlocked this Gag"""

    # TODO #29, Add Gag names to the Error messages
    def __init__(self, level, message="Gag is not unlocked yet"):
        self.level = level
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.level} -> {self.message}'


class LockedGagTrackError(GagCountError):
    """ Toon has not unlocked this Gag Track"""
    def __init__(self, track, message="Gag Track is not unlocked yet"):
        self.track = track
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.track} -> {self.message}'


class TooManyGagsError(GagCountError):
    """ Toon's Gag count exceeds Gag carry limit"""
    pass


class NotEnoughGagsError(GagCountError):
    """ Toon chooses a Gag with 0 quantity"""
    def __init__(self, gag: Gag=None, message="Insufficient Gag quantity"):
        self.gag = gag
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        err_msg = f'{self.gag.count} -> {self.message}'
        if self.gag:
            err_msg = f"Insufficient number of Gags: \"{self.gag.name}\","\
                    f"lvl {self.gag.level} {self.gag.track_name} count = "\
                    f" {self.gag.count}"
        return err_msg


class InvalidTargetError(Error):
    pass


class InvalidCogAttackTarget(InvalidTargetError):
    """ Cog targets a Cog or defeated Toon"""
    pass


class InvalidToonAttackTarget(InvalidTargetError):
    """ Toon targets a Toon or defeated Cog"""
    pass


class CogLuredError(InvalidToonAttackTarget):
    '''Toon uses a Lure or Trap on a lured Cog'''
    pass


class CogAlreadyTrappedError(InvalidToonAttackTarget):
    ''' Toon uses a Trap Gag on a trapped Cog'''
    pass


class InvalidAttackName(Error):
    pass


class InvalidAttackIndex(Error):
    '''Attack index is out of range, for either Toon/Cog'''
    pass


class InvalidAttackType(Error):
    """Set BattleEntity.attack to a non-Attack object"""
    pass


class InvalidToonHealTarget(InvalidTargetError):
    """ Toon targets a Cog or defeated Toon"""
    pass


class InvalidRelativeLevel(Error):
    """ Must be in range [0-4]"""
    def __init__(self, rel_lvl: int,
                 message="Relative level out of range: [0, 1, 2, 3, 4]"):
        self.rel_lvl = rel_lvl
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        err_msg = f"Relative level ({self.rel_lvl}) must be in the values " \
                  "[0, 1, 2, 3, 4], where 0 is the minimum Cog level and 4 " \
                  "is the maximum."
        return err_msg


class InvalidCogKey(Error):
    """ Cog key must be in `COG_ATTRIBUTES` dictionary"""
    pass


# TODO #9, Create test for this exception
class TargetDefeatedError(InvalidTargetError):
    """ Entity tries to attack a defeated Entity """
    pass
