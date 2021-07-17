from ...Toon import DEFAULT_HP, Inventory, Toon


NAME_DEFAULT = "Mickey"
NAME = "Astro"
HP = 65
LEVELS = [5, -1, 6, 5, 5, 5, 2]
EXPS = [7421, 0, 10101, 9443, 8690, 6862, 191]
GAGS = [[0,   0,  0,  5,  5,  3, -1],  # 0 TOON-UP
        [-1, -1, -1, -1, -1, -1, -1],  # 1 TRAP (LOCKED)
        [0,   0,  0,  0,  5,  3,  1],  # 2 LURE
        [0,   0,  0,  0,  5,  3, -1],  # 3 SOUND
        [0,   2,  1,  4,  4,  2, -1],  # 4 THROW
        [0,   0,  0,  5,  5,  3, -1],  # 5 SQUIRT
        [0,   9,  5, -1, -1, -1, -1]]  # 6 DROP
GAG_LIMIT = 70


class TestToonCreation:

    def test_toon_default_creation(self):
        t = Toon(name=NAME_DEFAULT)

        assert t.hp == DEFAULT_HP
        assert t.inventory == Inventory()

    def test_toon_astro_creation(self):
        astro_inventory = Inventory(
            gag_exps=EXPS, max_gags=GAG_LIMIT
        )
        astro = Toon(name=NAME, hp=HP, inventory=astro_inventory)

        # TODO Recreate Astro's Gags, need a way to convert list of Gag counts to List of Gags
        assert astro.name == NAME
        assert astro.hp == HP
