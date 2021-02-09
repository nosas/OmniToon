import pytest
from ...Cog import Cog
from ...CogGlobals import (
    COG_ATTRIBUTES, getActualFromRelativeLevel
)


@pytest.fixture
def cog_flunky_lvl2():
    cog_key = 'f'
    cog_name = COG_ATTRIBUTES[cog_key]['name']
    # Add 1 to cog_level because the level seems to also be used as index
    # EX: In-game, a level 5 Flunky would be coded to have cog.level==6
    # Therefore, a level 2 Flunky is coded to have cog.level==3
    # ! This is stupid and needs to be reworked.. I don't like this
    # We can consider Cogs having 5 tiers, from 0 -> 4
    rel_lvl = 1
    return Cog(key=cog_key, name=cog_name, relative_lvl=rel_lvl)


@pytest.fixture
def cog_flunky_lvl3():
    cog_key = 'f'
    cog_name = COG_ATTRIBUTES[cog_key]['name']
    rel_lvl = 2
    return Cog(key=cog_key, name=cog_name, relative_lvl=rel_lvl)


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
