import pytest
from ..fixtures.cog_fixtures import cog_flunky as cogf
from ...CogGlobals import COG_ATTRIBUTES, get_actual_from_relative_level


class TestCogGlobals:

    @pytest.mark.parametrize('cogf', [0], indirect=True)
    def test_cog_get_actual_from_relative_level(self, cogf):
        expected_lvl = 1
        exp_rel_lvl = 0

        actual_lvl = get_actual_from_relative_level(cog_key=cogf.key,
                                                    relative_level=exp_rel_lvl)
        assert actual_lvl == expected_lvl

    @pytest.mark.parametrize('cogf', [0], indirect=True)
    def test_cog_get_actual_from_relative_level_fail(self, cogf):
        for invalid_rel_lvl in [-1, 5]:
            with pytest.raises(AssertionError):
                get_actual_from_relative_level(cog_key=cogf.key,
                                               relative_level=invalid_rel_lvl)
