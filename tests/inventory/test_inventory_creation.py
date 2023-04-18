from src.core.Toon import Inventory
from src.core.ToonGlobals import DEFAULT_BEAN_COUNT, DEFAULT_BEAN_LIMIT
from src.gags.Gag import DEFAULT_TRACK_EXPS_CURRENT, Gags, get_default_gags
from src.gags.GagGlobals import DEFAULT_GAG_COUNT, DEFAULT_GAG_LIMIT


class TestInventoryDefaultCreation:
    inv = Inventory(gags=Gags(), max_gags=DEFAULT_GAG_LIMIT)

    def test_inventory_default_creation(self):
        assert self.inv.gags.gags == get_default_gags()
        assert self.inv.gags.gag_count == DEFAULT_GAG_COUNT
        assert self.inv.has_gags() is False
        assert self.inv.gags.track_exps == DEFAULT_TRACK_EXPS_CURRENT
        # assert self.inv.gag_exps_next == DEFAULT_TRACK_EXPS_NEXT

        assert self.inv.jellybeans == DEFAULT_BEAN_COUNT
        assert self.inv.max_jellybeans == DEFAULT_BEAN_LIMIT
        assert self.inv.max_gags == DEFAULT_GAG_LIMIT


class TestInventoryCreation:

    def test_inventory_type(self, inventory_astro: Inventory):
        assert isinstance(inventory_astro, Inventory)
        assert isinstance(inventory_astro.gags, Gags)
