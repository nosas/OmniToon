from builtins import Exception


class Error(Exception):
    pass


class GagCountError(Error):
    pass


class LockedGagError(GagCountError):
    """ Toon has not unlocked this Gag"""

    def __init__(self, gag_level, message="Gag is not unlocked yet`"):
        self.gag_level = gag_level
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.gag_level} -> {self.message}'


class LockedGagTrackError(GagCountError):
    """ Toon has not unlocked this Gag Track"""
    def __init__(self, gag_track, message="Gag Track is not unlocked yet`"):
        self.gag_track = gag_track
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.gag_track} -> {self.message}'


class TooManyGagsError(GagCountError):
    """ Toon's Gag count exceeds Gag carry limit"""
    pass


class NotEnoughGagsError(GagCountError):
    """ Toon chooses a Gag with 0 quantity"""
    pass


class InvalidTargetError(Error):
    pass


class InvalidCogAttackTarget(InvalidTargetError):
    """ Cog targets a Cog or defeated Toon"""
    pass


class InvalidToonAttackTarget(InvalidTargetError):
    """ Toon targets a Toon or defeated Cog"""
    pass


class InvalidToonHealTarget(InvalidTargetError):
    """ Toon targets a Cog or defeated Toon"""
    pass


class InvalidRelativeLevel(Error):
    """ Must be in range [0-4]"""
    pass
