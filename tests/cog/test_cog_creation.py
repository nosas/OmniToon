import pytest
from ..fixtures.cog_fixtures import cog_flunky
from ...Cog import Cog
from ...CogGlobals import COG_HP, COG_ATTRIBUTES


@pytest.mark.parametrize('cog_flunky', [0, 1, 2, 3, 4], indirect=True)
class TestFlunky:
    def test_flunky_name(self, cog_flunky: Cog):
        print(f"{cog_flunky.vitals}")
        assert cog_flunky.name == "Flunky"

    def test_flunky_key(self, cog_flunky: Cog):
        assert cog_flunky.key == 'f'

    def test_level(self, cog_flunky: Cog):
        min_level = COG_ATTRIBUTES[cog_flunky.key]['level']
        expected_level = min_level + cog_flunky.relative_level
        assert cog_flunky.level == expected_level

    def test_health(self, cog_flunky: Cog):
        cog_level = cog_flunky.level
        expected_hp = (cog_level + 1) * (cog_level + 2)
        assert cog_flunky.hp == expected_hp

        expected_hp = COG_HP[cog_flunky.level - 1]
        assert cog_flunky.hp == expected_hp
