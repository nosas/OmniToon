
from ...Gag import Gag
from ...GagGlobals import TRACK


EXP = 0
LEVEL = 0
HEAL_TRACK = TRACK.HEAL  # same as 0


class TestGagCreation:

    def test_gag_creation(self):
        g = Gag(exp=EXP, level=LEVEL, track=HEAL_TRACK)

        assert g.exp == EXP
        assert g.track == HEAL_TRACK
        assert g.level == LEVEL
        assert g.track_name == "Toon-Up"
