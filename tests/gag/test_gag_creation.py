from ...Attack import ATK_TGT_SINGLE
from ...Gag import Gag
from ...GagGlobals import THROW_TRACK, get_gag_damage


class TestGagCreation:

    def test_throw_gag_creation(self):
        t = Gag(track=THROW_TRACK, exp=100, level=0, count=10)
        assert t.track == THROW_TRACK
        assert t.track_name == 'Throw'
        assert t.name == 'Cupcake'
        assert t.level == 0
        assert t.count == 10
        assert t.damage == 6 == get_gag_damage(track=t.track, level=t.level, exp=t.exp)
        assert t.target == ATK_TGT_SINGLE
