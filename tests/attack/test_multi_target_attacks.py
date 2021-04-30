from ...BattleState import CogAttackState
from ...Battle import Battle
from ...Attack import ATK_TGT_MULTI, ATK_TGT_SINGLE
from ...GagGlobals import MULTI_TARGET_GAGS, get_gag_name, get_gag_target
from ..fixtures.cog_fixtures import cog_yesman
from ..fixtures.toon_fixtures import toon_astro, toon_ostra


class TestMultiTargetAttackProperties:

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


class TestMultiTargetAttackDamage:

    def test_cog_attack_damages_multiple_toons(self, cog_yesman, toon_astro,
                                               toon_ostra):
        battle = Battle(first_cog=cog_yesman, first_toon=toon_astro)
        battle.add_toon(toon_ostra)

        cog_yesman.manual_atk = cog_yesman.choose_attack("Synergy")
        atk_dmg = cog_yesman.manual_atk.damage

        battle.context.transition_to(CogAttackState())
        battle.update()

        for toon in [toon_astro, toon_ostra]:
            assert toon.hp == toon.hp_max - atk_dmg

        battle.context.transition_to(CogAttackState())
        battle.update()
        for toon in [toon_astro, toon_ostra]:
            assert toon.hp == toon.hp_max - (atk_dmg * 2)
