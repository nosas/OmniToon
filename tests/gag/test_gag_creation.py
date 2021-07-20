
from ...Gag import Gag, Gags
from ...GagGlobals import (DEFAULT_GAG_COUNT, DEFAULT_TRACK_EXPS_CURRENT,
                           DEFAULT_TRACK_LEVELS, GAG, TRACK)

EXP = 0
LEVEL = 0
HEAL_TRACK = TRACK.HEAL  # same as 0

# Astro-specific global variable
TRACK_EXPS = [7421, 0, 10101, 9443, 8690, 6862, 191]
GAG_COUNTS = [[0,   0,  0,  5,  5,  3, -1],  # 0 TOON-UP
              [-1, -1, -1, -1, -1, -1, -1],  # 1 TRAP (LOCKED)
              [0,   0,  0,  0,  5,  3,  1],  # 2 LURE
              [0,   0,  0,  0,  5,  3, -1],  # 3 SOUND
              [0,   2,  1,  4,  4,  2, -1],  # 4 THROW
              [0,   0,  0,  5,  5,  3, -1],  # 5 SQUIRT
              [0,   9,  5, -1, -1, -1, -1]]  # 6 DROP
EXPECTED_TRACK_LEVELS = [5, -1, 6, 5, 5, 5, 2]
EXPECTED_UNLOCKED_GAGS = 34
EXPECTED_AVAILABLE_GAGS = 18


class TestGagCreation:

    def test_gag_creation(self):
        g = Gag(exp=EXP, level=LEVEL, track=HEAL_TRACK)
        expected_gag = GAG.from_tuple((g.track, g.level))

        assert isinstance(g, Gag)
        assert g.exp == EXP
        assert g.track == HEAL_TRACK == expected_gag.track
        assert g.level == LEVEL == expected_gag .level
        assert g.name == expected_gag.name
        assert g.track.name == expected_gag.track.name


class TestGagsCreation:

    def test_gags_default_creation(self):
        gs = Gags(gag_count=DEFAULT_GAG_COUNT, track_exps=DEFAULT_TRACK_EXPS_CURRENT)

        assert all([isinstance(gag, Gag) for gag in gs])
        assert len([gag for gag in gs]) == 7*7
        assert len(gs.unlocked_gags) == 2
        assert len(gs.available_gags) == 0
        assert gs.gag_count == DEFAULT_GAG_COUNT
        assert gs.track_exps == DEFAULT_TRACK_EXPS_CURRENT
        assert gs.track_levels == DEFAULT_TRACK_LEVELS

    def test_gags_astro_creation(self):
        gs = Gags(gag_count=GAG_COUNTS, track_exps=TRACK_EXPS)

        assert len([gag for gag in gs]) == 7*7
        assert len(gs.unlocked_gags) == EXPECTED_UNLOCKED_GAGS
        assert len(gs.available_gags) == EXPECTED_AVAILABLE_GAGS
        assert gs.gag_count == GAG_COUNTS
        assert gs.track_exps == TRACK_EXPS
        assert gs.track_levels == EXPECTED_TRACK_LEVELS
