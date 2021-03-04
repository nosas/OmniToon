# %% Define imports, functions, and global variables

"""
BattleGlobalTracks = ['toon-up', 'trap', 'lure', 'sound', 'throw', 'squirt', 'drop']
BattleGlobalNPCTracks = ['restock', 'toons hit', 'cogs miss']
BattleGlobalAvPropStrings = (
 ('Feather', 'Megaphone', 'Lipstick', 'Bamboo Cane', 'Pixie Dust', 'Juggling Balls', 'High Dive'),
 ('Banana Peel', 'Rake', 'Marbles', 'Quicksand', 'Trapdoor', 'TNT', 'Railroad'),
 ('$1 bill', 'Small Magnet', '$5 bill', 'Big Magnet', '$10 bill', 'Hypno-goggles', 'Presentation'),
 ('Bike Horn', 'Whistle', 'Bugle', 'Aoogah', 'Elephant Trunk', 'Foghorn', 'Opera Singer'),
 ('Cupcake', 'Fruit Pie Slice', 'Cream Pie Slice', 'Whole Fruit Pie', 'Whole Cream Pie', 'Birthday Cake', 'Wedding Cake'),
 ('Squirting Flower', 'Glass of Water', 'Squirt Gun', 'Seltzer Bottle', 'Fire Hose', 'Storm Cloud', 'Geyser'),
 ('Flower Pot', 'Sandbag', 'Anvil', 'Big Weight', 'Safe', 'Grand Piano', 'Toontanic')
 )

"""  # noqa


from .GagGlobals import (
    GAG_TRACK_LABELS, get_gag_accuracy, get_gag_damage, get_gag_name
)


class GagTrack:
    def __init__(self, track, exp):
        self.track = track
        self.track_name = GAG_TRACK_LABELS[track]
        self.exp = exp
        # TODO Create `get_highest_level` func?


class Gag(GagTrack):
    def __init__(self, track, exp, level):
        """
        # TODO Review and fix docstring pls
        # TODO Create observer to monitor battles and determine viable gags
        :param int gag_track: Index of the gag_track (0-6)
        :param int level: Level of the current gag (0-6)
        :param int highest_level: Level of highest unlocked gag of same gtrack
        :param int/bool aoe: 0 if gag hits single targets, 1 for all targets
        :param int capacity_current: Current number of gags available
        """
        super().__init__(track=track, exp=exp)
        # ! Damage, quantity, capacity need to be dynamically updated after atk
        self.accuracy = get_gag_accuracy(gag_track=track, gag_level=level)
        self.damage = get_gag_damage(gag_track=track, gag_level=level, exp=exp)
        self.level = level
        self.name = get_gag_name(gag_track=track, gag_level=level)
        # self.highest_level = gag_track.highest_level
        # self.capacity_current = capacity_current
        # Maximum number of carryable gags of this level
        # self.capacity_maximum = 5 + (5*(highest_level-level))
