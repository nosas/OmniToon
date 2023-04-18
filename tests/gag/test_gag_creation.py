
from core.AttackGlobals import GROUP
from core.GagGlobals import (DEFAULT_GAG_COUNT, DEFAULT_TRACK_EXPS_CURRENT,
                             DEFAULT_TRACK_LEVELS, GAG, MULTI_TARGET_GAGS,
                             TRACK)
from core.ToonGlobals import (ASTRO_EXPECTED_AVAILABLE_GAGS,
                              ASTRO_EXPECTED_TRACK_LEVELS,
                              ASTRO_EXPECTED_UNLOCKED_GAGS, ASTRO_GAG_COUNT,
                              ASTRO_TRACK_EXPS)
from gags.Gag import Gag, Gags

EXP = 0
LEVEL = 0
HEAL_TRACK = TRACK.HEAL  # same as 0


class TestGagCreation:
    gag = Gag(exp=EXP, level=LEVEL, track=HEAL_TRACK)
    expected_gag = GAG.from_tuple((gag.track, gag.level))

    def test_gag_type(self):
        assert isinstance(self.gag, Gag)

    def test_gag_exp(self):
        assert self.gag.exp == EXP

    def test_gag_track(self):
        assert self.gag.track == HEAL_TRACK == self.expected_gag.track

    def test_gag_level(self):
        assert self.gag.level == LEVEL == self.expected_gag .level

    def test_gag_name(self):
        assert self.gag.name == self.expected_gag.name

    def test_gag_track_name(self):
        assert self.gag.track.name == self.expected_gag.track.name

    def test_multi_target_gag_creation(self):
        """Verify multi-targeted Gags have the proper gag.target attribute value"""
        mt_gags = [
            Gag(exp=0, level=gag_enum.level, track=gag_enum.track)
            for gag_enum in GAG
            if gag_enum.name in MULTI_TARGET_GAGS
        ]
        assert len(mt_gags) == len(MULTI_TARGET_GAGS)
        assert all([gag.target == GROUP.MULTI for gag in mt_gags])


class TestGagsDefaultCreation:
    gags = Gags(gag_count=DEFAULT_GAG_COUNT, track_exps=DEFAULT_TRACK_EXPS_CURRENT)

    def test_gags_type(self):
        assert all([isinstance(gag, Gag) for gag in self.gags])

    def test_gags_total_number_of_gags(self):
        assert len([gag for gag in self.gags]) == 7 * 7

    def test_gags_unlocked_gags(self):
        assert len(self.gags.unlocked_gags) == 2

    def test_gags_available_gags(self):
        assert len(self.gags.available_gags) == 0

    def test_gags_gag_count(self):
        assert self.gags.gag_count == DEFAULT_GAG_COUNT

    def test_gags_track_exps(self):
        assert self.gags.track_exps == DEFAULT_TRACK_EXPS_CURRENT

    def test_gags_track_levels(self):
        assert self.gags.track_levels == DEFAULT_TRACK_LEVELS


class TestGagsCreation:
    def test_gags_total_number_of_gags(self, gags_astro):
        assert len([gag for gag in gags_astro]) == 7 * 7

    def test_gags_unlocked_gags(self, gags_astro):
        assert len(gags_astro.unlocked_gags) == ASTRO_EXPECTED_UNLOCKED_GAGS

    def test_gags_available_gags(self, gags_astro):
        assert len(gags_astro.available_gags) == ASTRO_EXPECTED_AVAILABLE_GAGS

    def test_gags_gag_count(self, gags_astro):
        assert gags_astro.gag_count == ASTRO_GAG_COUNT

    def test_gags_track_exps(self, gags_astro):
        assert gags_astro.track_exps == ASTRO_TRACK_EXPS

    def test_gags_track_levels(self, gags_astro):
        assert gags_astro.track_levels == ASTRO_EXPECTED_TRACK_LEVELS
