import pytest

from Gag import Gags
from ToonGlobals import (ASTRO_GAG_COUNT, ASTRO_TRACK_EXPS, TRAPA_GAG_COUNT,
                            TRAPA_TRACK_EXPS)


@pytest.fixture
def gags_astro():
    gags = Gags(gag_count=ASTRO_GAG_COUNT, track_exps=ASTRO_TRACK_EXPS)
    return gags


@pytest.fixture
def gags_trapa():
    gags = Gags(gag_count=TRAPA_GAG_COUNT, track_exps=TRAPA_TRACK_EXPS)
    return gags
