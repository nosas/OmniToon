# %%
from .Entity import Entity
from .CogGlobals import (
    COG_ATTRIBUTES, get_cog_vitals, getActualFromRelativeLevel,
    CLIPON_TIE, POUND_KEY, SHRED
)


class Cog(Entity):
    def __init__(self, key, name, relative_level=-1):
        self.key = key
        self.name = name
        self.vitals = get_cog_vitals(cog_key=key, level=relative_level)
        self.hp = self.vitals['hp']
        # ! Relative level should be in range [0,4]
        self.relative_level = relative_level
        self.level = getActualFromRelativeLevel(cog_key=key,
                                                rel_lvl=relative_level)
        super().__init__(name=self.name, hp=self.hp)
