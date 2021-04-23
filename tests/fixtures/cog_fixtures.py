import pytest

from ...Cog import Cog
from ...CogGlobals import COG_ATTRIBUTES


@pytest.fixture
# https://stackoverflow.com/questions/42228895/how-to-parametrize-a-pytest-fixture  # noqa
def cog_flunky(request):
    """Yields a Flunky Cog object when passed a relative_level [0-4] argument.
        NOTE: This function was created so I could parametrize the `cog_flunky`
        fixture and test every level Flunky.

    Example Usage from `test_cog_attack.py`:
        from ..fixtures.cog_fixtures import cog_flunky as cogf
        @pytest.mark.parametrize('cogf', [0, 1, 2, 3, 4], indirect=True)
        class TestCogAttack:

    Args:
        request ([type]): [description]

    Yields:
        Cog: [description]
    """
    cog_key = 'f'
    cog_name = COG_ATTRIBUTES[cog_key]['name']
    try:
        cog_flunky = Cog(key=cog_key, name=cog_name,
                         relative_level=request.param)
    except AttributeError as e:
        print("[!] WARNING : No relative `cog_level` was provided, returning "
              f"default level of 0, in test {request.function}")
        cog_flunky = Cog(key=cog_key, name=cog_name)

    yield cog_flunky


def cog_yesman(request):
    '''
    'ym': {
        'name': 'Yesman',
        'level': 3,
        'hp': COG_HP[2:7],
        'def': (10, 15, 20, 25, 30),
        'freq': (50, 30, 10, 5, 5),
        'acc': (65, 70, 75, 80, 85),
        'attacks': (
            ('RubberStamp', ATK_TGT_SINGLE,
                (2, 2, 3, 3, 4),
                (75, 75, 75, 75, 75),
                (35, 35, 35, 35, 35)),
            ('RazzleDazzle', ATK_TGT_SINGLE,
                (1, 1, 1, 1, 1),
                (50, 50, 50, 50, 50),
                (25, 20, 15, 10, 5)),
            ('Synergy', ATK_TGT_MULTI,
                (4, 5, 6, 7, 8),
                (50, 60, 70, 80, 90),
                (5, 10, 15, 20, 25)),
            ('TeeOff', ATK_TGT_SINGLE,
                (3, 3, 4, 4, 5),
                (50, 60, 70, 80, 90),
                (35, 35, 35, 35, 35))
        )
    },
    '''
    cog_key = 'ym'
    cog_name = COG_ATTRIBUTES[cog_key]['name']
    try:
        cog_yesman = Cog(key=cog_key, name=cog_name,
                         relative_level=request.param)
    except AttributeError as e:
        print("[!] WARNING : No relative `cog_level` was provided, returning "
              f"default level of 0, in test {request.function}")
        cog_yesman = Cog(key=cog_key, name=cog_name)

    yield cog_yesman
