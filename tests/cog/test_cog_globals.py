import pytest
from ..fixtures.cog_fixtures import cog_flunky as cogf
from ...CogGlobals import COG_ATTRIBUTES, get_actual_from_relative_level

EXPECTED_REL_LVL = 0

@pytest.mark.parametrize('cogf', [EXPECTED_REL_LVL], indirect=True)
class TestCogGlobals:

    @pytest.mark.parametrize(['exp_rel_lvl', 'exp_actual_lvl'],
                             [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
    def test_cog_get_actual_from_relative_level(self, cogf, exp_rel_lvl,
                                                exp_actual_lvl):
        actual_lvl = get_actual_from_relative_level(cog_key=cogf.key,
                                                    relative_level=exp_rel_lvl)
        assert actual_lvl == exp_actual_lvl

    @pytest.mark.parametrize('invalid_rel_lvl', [-1, 5])
    def test_cog_get_actual_from_relative_level_fail(self, cogf,
                                                     invalid_rel_lvl):
        with pytest.raises(AssertionError):
            get_actual_from_relative_level(cog_key=cogf.key,
                                           relative_level=invalid_rel_lvl)

    def test_cog_attack(self, cogf):
        pass
