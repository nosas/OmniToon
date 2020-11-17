from Toon import Toon
from Cog import Cog


def play(toon, cog):
    # While the Toon is not dead, continue battling
    while not toon.is_dead():
        toon.do_attack(target=cog, amount=1)
