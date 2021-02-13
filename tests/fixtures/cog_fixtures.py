import pytest
from ...Cog import Cog
from ...CogGlobals import COG_ATTRIBUTES


@pytest.fixture
# https://stackoverflow.com/questions/42228895/how-to-parametrize-a-pytest-fixture  # noqa
def cog_flunky(request):
    cog_key = 'f'
    cog_name = COG_ATTRIBUTES[cog_key]['name']
    cog_flunky = Cog(key=cog_key, name=cog_name, relative_level=request.param)
    yield cog_flunky


@pytest.fixture
def cog_flunky_lvl2():
    cog_key = 'f'
    cog_name = COG_ATTRIBUTES[cog_key]['name']
    # Add 1 to cog_level because the level seems to also be used as index
    # EX: In-game, a level 5 Flunky would be coded to have cog.level==6
    # ? Is this still true??
    # Therefore, a level 2 Flunky is coded to have cog.level==3
    # ! This is stupid and needs to be reworked.. I don't like this
    # We can consider Cogs having 5 tiers, from 0 -> 4
    relative_level = 1
    cog_flunky_lvl2 = Cog(key=cog_key, name=cog_name,
                          relative_level=relative_level)
    yield cog_flunky_lvl2


@pytest.fixture
def cog_flunky_lvl3():
    cog_key = 'f'
    cog_name = COG_ATTRIBUTES[cog_key]['name']
    relative_level = 2
    cog_flunky_lvl3 = Cog(key=cog_key, name=cog_name,
                          relative_level=relative_level)
    yield cog_flunky_lvl3
