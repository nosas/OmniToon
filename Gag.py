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

from .Attack import Attack
from .GagGlobals import (get_gag_accuracy, get_gag_damage, get_gag_name,
                         get_gag_target, get_gag_track_name)


class Gag(Attack):
    def __init__(self, track: int, exp: int, level: int, count: int = 0):
        """
        # TODO Review and fix docstring pls
        # TODO #25, Create observer to monitor battles & determine viable Gags
        """
        self.track = track
        self.level = level
        name = get_gag_name(track=track, level=level)
        # ! Damage, quantity, capacity need to be dynamically updated after atk
        super().__init__(
            name=name,
            damage=get_gag_damage(track=track, level=level, exp=exp),
            accuracy=get_gag_accuracy(track=track, level=level),
            target=get_gag_target(name=name))

        self.track_name = get_gag_track_name(track=track)
        self.exp = exp
        self.count = count

        # Trap-specific attributes used for tracking EXP rewards
        self._is_attack = False
        self._is_setup = False

    @property
    def is_attack(self) -> bool:
        return self._is_attack

    @is_attack.setter
    def is_attack(self, new_is_attack: bool) -> None:
        assert type(new_is_attack) == bool

        print(f"                [>] is_attack : {self.is_attack} -> {new_is_attack} on {self}")  # noqa
        self._is_attack = new_is_attack

    @property
    def is_setup(self) -> bool:
        return self._is_setup

    @is_setup.setter
    def is_setup(self, new_is_setup: bool) -> None:
        assert type(new_is_setup) == bool
        print(f"                [>] is_setup : {self.is_setup} -> {new_is_setup} on {self}")  # noqa
        self._is_setup = new_is_setup

        # TODO Create function to get max count
        # Maximum number of carryable gags of this level
        # self.capacity_maximum = 5 + (5*(highest_level-level))

    def __str__(self):
        # print(gag_throw) == 'Lvl 3 Throw, "Whole Fruit Pie" (2million dmg)'
        return f'lvl {self.level} {self.track_name} '\
               f'"{self.name}" ({self.track, self.level}, {self.damage}dmg)'

    def __repr__(self):
        # repr(gag_throw) == (track_idx, level, exp, damage_min, damage_max,
        #                     damage, accuracy, count_current, count_max)
        return f'Gag(track_name="{self.track_name}", track={self.track}, '\
               f'level={self.level}, name="{self.name}", count={self.count}, '\
               f'damage={self.damage}, exp={self.exp}, setup={self.is_setup},'\
               f' attack={self.is_attack})'
