from ..fixtures.cog_fixtures import cog_flunky_lvl2, cog_flunky_lvl3


class TestFlunkyLvl2:
    def test_key(self, cog_flunky_lvl2):
        assert cog_flunky_lvl2.key == "f"

    def test_name(self, cog_flunky_lvl2):
        assert cog_flunky_lvl2.name == "Flunky"

    def test_level(self, cog_flunky_lvl2):
        assert cog_flunky_lvl2.level == 2

    def test_health(self, cog_flunky_lvl2):
        cog_level = cog_flunky_lvl2.level
        expected_hp = (cog_level + 1) * (cog_level + 2)
        assert cog_flunky_lvl2.hp == expected_hp


class TestFlunkyLvl3:
    def test_key(self, cog_flunky_lvl3):
        assert cog_flunky_lvl3.key == "f"

    def test_name(self, cog_flunky_lvl3):
        assert cog_flunky_lvl3.name == "Flunky"

    def test_level(self, cog_flunky_lvl3):
        assert cog_flunky_lvl3.level == 3

    def test_health(self, cog_flunky_lvl3):
        cog_level = cog_flunky_lvl3.level
        expected_hp = (cog_level + 1) * (cog_level + 2)
        assert cog_flunky_lvl3.hp == expected_hp
