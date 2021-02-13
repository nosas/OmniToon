# %%
# Python Imports how-to : https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time  # noqa
from .Toon import Toon
from .Cog import Cog
from .GagGlobals import (
    HEAL_TRACK, TRAP_TRACK, LURE_TRACK, SOUND_TRACK, THROW_TRACK, SQUIRT_TRACK,
    DROP_TRACK, get_gag_damage
)
from .CogGlobals import (
    COG_ATTRIBUTES, get_cog_vitals, pick_cog_attack, get_cog_attack
)


def play(toon, cog):
    # While the Toon is not dead, continue battling
    while not toon.is_dead():
        toon.do_attack(target=cog, amount=1)


def test_fight():
    name = "Astro"
    health = "65"
    levels = [5, 0, 6, 5, 5, 5, 2]
    exps = [7421, 0, 10101, 9443, 8690, 6862, 191]

    # TODO Create proper test for Toon object creation
    # gags = [[1]*7] + [[0]*7]*6  # 7 total Gags
    gags = [[10]*7] + [[0]*7]*6   # 70 total Gags
    gag_limit = 70    # Expect pass
    # gag_limit = 71  # Expect pass
    # gag_limit = 69  # Expect failure
    my_toon = Toon(name=name, health=health, gags=gags, gag_limit=gag_limit,
                   gag_levels=levels, gag_exps=exps)

    num_all_gags = my_toon.count_all_gags(my_toon.gags)
    print(f"Toon {name} has Gags? {my_toon.has_gags()} {num_all_gags}")

    has_gag = my_toon.has_gag(gag_track=0, gag=0)
    num_gags = my_toon.count_gag(gag_track=0, gag=0)
    print(f"Toon {name} has Toon-Up Gag? {has_gag} {num_gags}")

    name = 'f'
    relative_level = 1
    flunky_vitals = get_cog_vitals(name=name, relative_level=relative_level)

    cog = Cog(name=name, vitals=flunky_vitals, relative_level=relative_level)


# %%
