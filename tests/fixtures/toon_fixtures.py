import pytest

from ...Toon import Toon


@pytest.fixture
def toon_astro():
    name = "Astro"
    hp = 65
    levels = [5, -1, 6, 5, 5, 5, 2]
    exps = [7421, 0, 10101, 9443, 8690, 6862, 191]
    gags = [[0,   0,  0,  5,  5,  3, -1],  # 0 Toon-up
            [-1, -1, -1, -1, -1, -1, -1],  # 1 Trap (locked)
            [0,   0,  0,  0,  5,  3,  1],  # 2 Lure
            [0,   0,  0,  0,  5,  3, -1],  # 3 Sound
            [0,   2,  1,  4,  4,  2, -1],  # 4 Throw
            [0,   0,  0,  5,  5,  3, -1],  # 5 Squirt
            [0,   9,  5, -1, -1, -1, -1]]  # 6 Drop
    gag_limit = 70

    return Toon(name=name, hp=hp, gags=gags, gag_limit=gag_limit,
                gag_levels=levels, gag_exps=exps)


@pytest.fixture
def toon_ostra():
    name = "Ostra"
    hp = 69
    levels = [5, 2, 6, 5, 5, 5, -1]
    exps = [7421, 191, 10101, 9443, 8690, 6862, 0]
    gags = [[0,   0,  0,  5,  5,  3, -1],  # 0 Toon-up
            [0,   9,  5, -1, -1, -1, -1],  # 1 Trap
            [0,   0,  0,  0,  5,  3,  1],  # 2 Lure
            [0,   0,  0,  0,  5,  3, -1],  # 3 Sound
            [0,   2,  1,  4,  4,  2, -1],  # 4 Throw
            [0,   0,  0,  5,  5,  3, -1],  # 5 Squirt
            [-1, -1, -1, -1, -1, -1, -1]]  # 6 Drop (locked)
    gag_limit = 70

    return Toon(name=name, hp=hp, gags=gags, gag_limit=gag_limit,
                gag_levels=levels, gag_exps=exps)


@pytest.fixture
def toon_newbi():
    name = "Newbi"
    hp = 22
    level = [-1, -1, -1, -1, 2, 2, -1]
    exps = [0, 0, 0, 0, 69, 420, 0]
    gags = [[-1, -1, -1, -1, -1, -1, -1],  # 0 Toon-up
            [-1, -1, -1, -1, -1, -1, -1],  # 1 Trap
            [-1, -1, -1, -1, -1, -1, -1],  # 2 Lure
            [-1, -1, -1, -1, -1, -1, -1],  # 3 Sound
            [0, 5, 5, -1, -1, -1, -1],  # 4 Throw
            [5, 10, 5, -1, -1, -1, -1],  # 5 Squirt
            [-1, -1, -1, -1, -1, -1, -1]]  # 6 Drop
    gag_limit = 30

    return Toon(name=name, hp=hp, gags=gags, gag_limit=gag_limit,
                gag_levels=level, gag_exps=exps)


@pytest.fixture
def toon_sport():
    name = "Sport"
    hp = 99
    level = [6, 6, 6, 6, 6, 6, -1]
    exps = [10000, 10000, 10000, 10000, 10000, 10000, 0]
    gags = [[10, 5, 4, 5, 5, 3, 1],  # 0 Toon-up
            [5, 5, 4, 5, 5, 3, 1],  # 1 Trap
            [10, 5, 4, 5, 5, 3, 1],  # 2 Lure
            [1, 1, 0, 0, 0, 0, 0, 0],  # 3 Sound
            [1, 1, 0, 0, 0, 0, 0, 0],  # 4 Throw
            [1, 1, 0, 0, 0, 0, 0, 0],  # 5 Squirt
            [-1, -1, -1, -1, -1, -1, -1]]  # 6 Drop
    gag_limit = 100

    return Toon(name=name, hp=hp, gags=gags, gag_limit=gag_limit,
                gag_levels=level, gag_exps=exps)


@pytest.fixture
def toon_default():
    return Toon(name="Mickey Mouse")
