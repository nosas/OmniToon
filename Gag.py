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


class GagTrack:
    def __init__(self, gtrack):
        self.gtrack = gtrack
        self.highest_level = 1
        self.xp_current = 0
        self.xp_needed = 10


class Gag(GagTrack):
    def __init__(self, gtrack, name, level, highest_level, capacity_current,
                 base_damage):
        """
        :param GagTrack gtrack: Type of the gag (throw, squirt, toon-up, etc.)
        :param int level: Level of the current gag (0-6)
        :param int highest_level: Level of highest unlocked gag of same gtrack
        :param int/bool aoe: 0 if gag hits single targets, 1 for all targets
        :param int capacity_current: Current number of gags available
        :param int xp_needed: XP needed to advance to use this gag
        :param int xp_provided: XP provided after attacking with this gag
        :param int min_cog_level: Minimum cog level required to receive XP
        """
        super().__init__(gtrack=gtrack)
        self.name = name
        self.level = level
        self.highest_level = gtrack.highest_level
        self.capacity_current = capacity_current
        # Maximum number of carryable gags of this level
        self.capacity_maximum = 5 + (5*(highest_level-level))
