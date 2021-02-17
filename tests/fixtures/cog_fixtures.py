import pytest
from ...Cog import Cog
from ...CogGlobals import COG_ATTRIBUTES


@pytest.fixture
# https://stackoverflow.com/questions/42228895/how-to-parametrize-a-pytest-fixture  # noqa
def cog_flunky(request):
    cog_key = 'f'
    cog_name = COG_ATTRIBUTES[cog_key]['name']
    try:
        cog_flunky = Cog(key=cog_key, name=cog_name,
                         relative_level=request.param)
    except AttributeError as e:
        print("[!] WARNING : No relative cog_level was provided, returning "
              f"default level of 0, in test {request.function}")
        cog_flunky = Cog(key=cog_key, name=cog_name)

    yield cog_flunky
