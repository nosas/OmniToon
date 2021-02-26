from .Entity import Entity
from .CogGlobals import get_cog_vitals, get_actual_from_relative_level


class Cog(Entity):
    def __init__(self, key, name, relative_level=0):
        self.key = key
        self.name = name
        self.vitals = get_cog_vitals(cog_key=key,
                                     relative_level=relative_level)
        self.hp = self.vitals['hp']
        # ! Relative level should be in range [0,4]
        self.relative_level = relative_level
        self.level = get_actual_from_relative_level(
            cog_key=key, relative_level=relative_level)
        super().__init__(name=self.name, hp=self.hp)

    def get_all_attacks(self):
        """[summary]

        Returns:
            [type]: [description]
            Example: 'attacks': [
                {
                    'acc': 75,
                    'animName': 'phone',
                    'freq': 30,
                    'hp': 2,
                    'id': 0,
                    'name': 'PoundKey'
                    'target': 2,
                },
                {
                    'acc': 50,
                    'animName': 'shredder',
                    'freq': 10,
                    'hp': 3,
                    'id': 1,
                    'name': 'Shred'
                    'target': 2,
                },
                {
                    'acc': 75,
                    'animName': 'throw-paper',
                    'freq': 60,
                    'hp': 1,
                    'id': 2,
                    'name': 'ClipOnTie'
                    'target': 2,
                }
            ]
        """
        return self.vitals['attacks']

    def get_attack(self, attack_index):
        """[summary]
        Args:
            attack_index ([type]): [description]

        Returns:
            dict: Dictionary containing all attributes of a single Cog's attack
        Example ::
            {
                'acc': 80,
                'animName': 'phone',
                'freq': 40,
                'hp': 3,
                'id': 0,
                'name': 'PoundKey',
                'target': 2  # ATK_TGT_SINGLE=1, ATK_TGT_GROUP=2
            }
        """
        return self.vitals['attacks'][attack_index]
