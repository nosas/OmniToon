import pytest

from ...Gag import Gags
from ...ToonGlobals import ASTRO_GAG_COUNT, ASTRO_TRACK_EXPS


@pytest.fixture
def gags_astro():
    gags = Gags(gag_count=ASTRO_GAG_COUNT, track_exps=ASTRO_TRACK_EXPS)
    return gags
