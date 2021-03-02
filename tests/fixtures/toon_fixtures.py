import pytest
from ...Toon import Toon


@pytest.fixture
def toon_astro():
    name = "Astro"
    hp = 65
    levels = [5, 0, 6, 5, 5, 5, 2]
    exps = [7421, 0, 10101, 9443, 8690, 6862, 191]
    gags = [[0, 0, 0, 5, 5, 3, 0],  # Toon-up
            [0, 0, 0, 0, 0, 0, 0],  # Trap
            [0, 0, 0, 0, 5, 3, 1],  # Lure
            [0, 0, 0, 0, 5, 3, 0],  # Sound
            [0, 2, 1, 4, 4, 2, 0],  # Throw
            [0, 0, 0, 5, 5, 3, 0],  # Squirt
            [0, 9, 5, 0, 0, 0, 0]]  # Drop
    gag_limit = 70

    return Toon(name=name, hp=hp, gags=gags, gag_limit=gag_limit,
                gag_levels=levels, gag_exps=exps)


@pytest.fixture
def toon_default():
    return Toon(name="Mickey Mouse")
