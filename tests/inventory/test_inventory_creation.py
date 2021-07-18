from ...Gag import DEFAULT_TRACK_EXPS_CURRENT, Gags, get_default_gags
from ...GagGlobals import DEFAULT_GAG_COUNT
from ...Toon import (DEFAULT_BEAN_COUNT, DEFAULT_BEAN_LIMIT, DEFAULT_GAG_LIMIT,
                     Inventory)


class TestInventoryCreation:

    def test_inventory_default_creation(self):
        gs = Gags(gag_count=DEFAULT_GAG_COUNT, track_exps=DEFAULT_TRACK_EXPS_CURRENT)
        i = Inventory(gags=gs, max_gags=DEFAULT_GAG_LIMIT)
        assert i.gags.gags == get_default_gags()
        assert i.gags.track_exps == DEFAULT_TRACK_EXPS_CURRENT
        # assert i.gag_exps_next == DEFAULT_TRACK_EXPS_NEXT

        assert i.jellybeans == DEFAULT_BEAN_COUNT
        assert i.max_jellybeans == DEFAULT_BEAN_LIMIT
        assert i.max_gags == DEFAULT_GAG_LIMIT
