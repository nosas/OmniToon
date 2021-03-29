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


from .GagGlobals import (GAG_TRACK_LABELS, get_gag_accuracy, get_gag_damage,
                         get_gag_name)


class GagTrack:
    def __init__(self, track, exp):
        self.track = track
        self.track_name = GAG_TRACK_LABELS[track]
        self.exp = exp


class Gag(GagTrack):
    def __init__(self, track, exp, level, count=0):
        """
        # TODO Review and fix docstring pls
        # TODO #25, Create observer to monitor battles & determine viable Gags
        """
        super().__init__(track=track, exp=exp)
        # ! Damage, quantity, capacity need to be dynamically updated after atk
        self.accuracy = get_gag_accuracy(track=track, level=level)
        self.count = count
        self.damage = get_gag_damage(track=track, level=level, exp=exp)
        self.level = level
        self.name = get_gag_name(track=track, level=level)
        # TODO Create function to get max count
        # Maximum number of carryable gags of this level
        # self.capacity_maximum = 5 + (5*(highest_level-level))

    def __str__(self):
        # print(gag_throw) == 'Lvl 3 Throw, "Whole Fruit Pie" (2million dmg)'
        return f'lvl {self.level} {self.track_name} ({self.track}) '\
               f'"{self.name}" ({self.damage}dmg)'

    def __repr__(self):
        # repr(gag_throw) == (track_idx, level, exp, damage_min, damage_max,
        #                     damage, accuracy, count_current, count_max)
        return f'Gag(track_name="{self.track_name}", track={self.track}, '\
               f'level={self.level}, name="{self.name}", count={self.count}, '\
               f'damage={self.damage}, exp={self.exp})'
