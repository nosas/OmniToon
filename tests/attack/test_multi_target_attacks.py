from ...Attack import ATK_TGT_MULTI, ATK_TGT_SINGLE
from ...GagGlobals import MULTI_TARGET_GAGS, get_gag_name, get_gag_target
from ..fixtures.cog_fixtures import cog_yesman


class TestMultiTargetAttacks:

    def test_cog_attack_is_multi_target(self, cog_yesman):
        # cog_atk = cog_yesman.choose_attack("Synergy")
        for cog_atk in cog_yesman.attacks:
            expected_target = (ATK_TGT_MULTI
                               if cog_atk['name'] == "Synergy"
                               else ATK_TGT_SINGLE)
            assert cog_atk['target'] == expected_target

    def test_toon_attack_is_multi_target(self):
        for gag_track in range(6):
            for gag_level in range(6):
                gag_name = get_gag_name(track=gag_track, level=gag_level)
                gag_target = get_gag_target(name=gag_name)
                expected_target = (ATK_TGT_MULTI
                                   if gag_name in MULTI_TARGET_GAGS
                                   else ATK_TGT_SINGLE)

                assert gag_target == expected_target
