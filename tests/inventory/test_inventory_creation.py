from ...Toon import (DEFAULT_BEAN_COUNT, DEFAULT_BEAN_LIMIT, DEFAULT_GAG_LIMIT,
                     DEFAULT_TRACK_EXPS_CURRENT, DEFAULT_TRACK_EXPS_NEXT,
                     Inventory, get_default_gags)


class TestInventoryCreation:

    def test_inventory_default_creation(self):
        i = Inventory()
        assert i._gags == get_default_gags()
        assert i.gag_exps == DEFAULT_TRACK_EXPS_CURRENT
        assert i.gag_exps_next == DEFAULT_TRACK_EXPS_NEXT

        assert i.jellybeans == DEFAULT_BEAN_COUNT
        assert i.max_jellybeans == DEFAULT_BEAN_LIMIT
        assert i.max_gags == DEFAULT_GAG_LIMIT
