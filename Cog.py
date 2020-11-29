# %%
from ttr_ai.Entity import Entity
from ttr_ai.CogGlobals import (
    COG_ATTRIBUTES, get_cog_vitals, pick_cog_attack, get_cog_attack,
    CLIPON_TIE, POUND_KEY, SHRED
)


class Cog(Entity):
    def __init__(self, name, vitals, level):
        self.name = name
        self.vitals = vitals
        self.level = level
        self.hp = vitals['hp']
        super().__init__(name=self.name, hp=self.hp)


name = 'f'
cog_info = COG_ATTRIBUTES[name]
cog_name = cog_info['name']
level = 2
flunky_vitals = get_cog_vitals(name=name, level=level)

cog = Cog(name=name, vitals=flunky_vitals, level=level)
print(cog.hp)
# Selects a random attack based on freq unless `attackNum` argument is passed
attack = get_cog_attack(suitName=cog.name, suitLevel=cog.level)
print(attack)
# ! Cannot use argument: attacks=cog.vitals['attacks']. Expects 2-D Tuple, not list of dicts  # noqa
# vitals['attacks'] = [{'name': 'PoundKey','animName': 'phone','hp': 3,'acc': 80,'freq': 40,'group': 2},{'name': 'Shred'}, {'name': 'ClipOnTie'}]  # noqa
# COG_ATTRIBUTES[name]['attacks'] = (('PoundKey', (2, 2, 3, 4, 6), (75, 75, 80, 80, 90), (30, 35, 40, 45, 50)), ....)  # noqa
attack = pick_cog_attack(attacks=COG_ATTRIBUTES[name]['attacks'],
                         suitLevel=cog.level)
print(attack)
# %%
print("id,name,hp,acc,freq")
for attackNum in [CLIPON_TIE, POUND_KEY, SHRED]:
    attack = get_cog_attack(suitName=cog.name,
                            suitLevel=cog.level,
                            attackNum=attackNum)
    print(f"{attack['id']},{attack['name']},{attack['hp']},{attack['acc']},{attack['freq']}")  # noqa

# %%

# %%
