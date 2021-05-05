import pytest

from ...Attack import ATK_TGT_SINGLE
from ...CogGlobals import (ATK_IDX_ACC, ATK_IDX_DMG, ATK_IDX_FREQ,
                           ATK_IDX_NAME, ATK_IDX_TGT, COG_ATTRIBUTES,
                           get_actual_from_relative_level, get_cog_attack,
                           get_cog_attacks_all_levels, get_cog_vitals)
from ...Exceptions import (InvalidAttackIndex, InvalidCogKey,
                           InvalidRelativeLevel)
from ..fixtures.cog_fixtures import cog_flunky as cogf

EXPECTED_REL_LVL = 0
INVALID_COG_KEY = 'zzz'
INVALID_FLUNKY_ATK_IDX = 3
INVALID_REL_LVLS = [-1, -2, 5]
# get_cog_attack
EXP_ATKS = [
    (
        'PoundKey', ATK_TGT_SINGLE,             # name, target
        (2, 2, 3, 4, 6), (75, 75, 80, 80, 90),  # dmg[rel_lvl], acc[rel_lvl]
        (30, 35, 40, 45, 50)),                  # freq[rel_lvl]
    (
        'Shred', ATK_TGT_SINGLE,
        (3, 4, 5, 6, 7), (50, 55, 60, 65, 70),
        (10, 15, 20, 25, 30)),
    (
        'ClipOnTie', ATK_TGT_SINGLE,
        (1, 1, 2, 2, 3), (75, 80, 85, 90, 95),
        (60, 50, 40, 30, 20))
    ]

@pytest.mark.parametrize('cogf', [EXPECTED_REL_LVL], indirect=True)
class TestCogGlobals:

    @pytest.mark.parametrize(['exp_rel_lvl', 'exp_actual_lvl'],
                             [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
    def test_cog_get_actual_from_relative_level(self, cogf, exp_rel_lvl,
                                                exp_actual_lvl):
        actual_lvl = get_actual_from_relative_level(cog_key=cogf.key,
                                                    relative_level=exp_rel_lvl)
        assert actual_lvl == exp_actual_lvl

    def test_cog_get_actual_from_relative_level_fail_key(self, cogf):
        with pytest.raises(InvalidCogKey):
            get_actual_from_relative_level(cog_key=INVALID_COG_KEY,
                                           relative_level=cogf.relative_level)

    @pytest.mark.parametrize('invalid_rel_lvl', INVALID_REL_LVLS)
    def test_cog_get_actual_from_relative_level_fail_lvl(self, cogf,
                                                         invalid_rel_lvl):
        with pytest.raises(InvalidRelativeLevel):
            get_actual_from_relative_level(cog_key=cogf.key,
                                           relative_level=invalid_rel_lvl)

    @pytest.mark.parametrize('atk_idx, exp_acc',
                             [(0, EXP_ATKS[0][ATK_IDX_ACC][EXPECTED_REL_LVL]),
                              (1, EXP_ATKS[1][ATK_IDX_ACC][EXPECTED_REL_LVL]),
                              (2, EXP_ATKS[2][ATK_IDX_ACC][EXPECTED_REL_LVL])])
    def test_get_cog_attack_acc(self, cogf, atk_idx, exp_acc):
        cog_atk = get_cog_attack(cog_key=cogf.key,
                                 relative_level=cogf.relative_level,
                                 attack_index=atk_idx)
        assert cog_atk['acc'] == exp_acc

    @pytest.mark.parametrize('atk_idx, exp_dmg',
                             [(0, EXP_ATKS[0][ATK_IDX_DMG][EXPECTED_REL_LVL]),
                              (1, EXP_ATKS[1][ATK_IDX_DMG][EXPECTED_REL_LVL]),
                              (2, EXP_ATKS[2][ATK_IDX_DMG][EXPECTED_REL_LVL])])
    def test_get_cog_attack_dmg(self, cogf, atk_idx, exp_dmg):
        cog_atk = get_cog_attack(cog_key=cogf.key,
                                 relative_level=cogf.relative_level,
                                 attack_index=atk_idx)
        assert cog_atk['damage'] == exp_dmg

    def test_get_cog_attack_fail_index(self, cogf):
        with pytest.raises(InvalidAttackIndex):
            get_cog_attack(cog_key=cogf.key,
                           relative_level=cogf.relative_level,
                           attack_index=INVALID_FLUNKY_ATK_IDX)

    def test_get_cog_attack_fail_key(self, cogf):
        with pytest.raises(InvalidCogKey):
            get_cog_attack(cog_key=INVALID_COG_KEY,
                           relative_level=cogf.relative_level)

    @pytest.mark.parametrize('invalid_rel_lvl', INVALID_REL_LVLS)
    def test_get_cog_attack_fail_level(self, cogf, invalid_rel_lvl):
        with pytest.raises(InvalidRelativeLevel):
            get_cog_attack(cog_key=cogf.key,
                           relative_level=invalid_rel_lvl)

    @pytest.mark.parametrize('atk_idx, exp_freq',
                             [(0, EXP_ATKS[0][ATK_IDX_FREQ][EXPECTED_REL_LVL]),
                              (1, EXP_ATKS[1][ATK_IDX_FREQ][EXPECTED_REL_LVL]),
                              (2, EXP_ATKS[2][ATK_IDX_FREQ][EXPECTED_REL_LVL])
                              ])
    def test_get_cog_attack_freq(self, cogf, atk_idx, exp_freq):
        cog_atk = get_cog_attack(cog_key=cogf.key,
                                 relative_level=cogf.relative_level,
                                 attack_index=atk_idx)
        assert cog_atk['freq'] == exp_freq

    @pytest.mark.parametrize('atk_idx, exp_name',
                             [(0, EXP_ATKS[0][ATK_IDX_NAME]),
                              (1, EXP_ATKS[1][ATK_IDX_NAME]),
                              (2, EXP_ATKS[2][ATK_IDX_NAME])])
    def test_get_cog_attack_name(self, cogf, atk_idx, exp_name):
        cog_atk = get_cog_attack(cog_key=cogf.key,
                                 relative_level=cogf.relative_level,
                                 attack_index=atk_idx)
        assert cog_atk['name'] == exp_name

    @pytest.mark.parametrize('atk_idx, exp_tgt',
                             [(0, EXP_ATKS[0][ATK_IDX_TGT]),
                              (1, EXP_ATKS[1][ATK_IDX_TGT]),
                              (2, EXP_ATKS[2][ATK_IDX_TGT])])
    def test_get_cog_attack_tgt(self, cogf, atk_idx, exp_tgt):
        cog_atk = get_cog_attack(cog_key=cogf.key,
                                 relative_level=cogf.relative_level,
                                 attack_index=atk_idx)
        assert cog_atk['target'] == exp_tgt

    def test_get_cog_attacks_all_levels(self, cogf):
        all_attacks = get_cog_attacks_all_levels(cog_key=cogf.key)
        for attack in all_attacks:
            assert attack in EXP_ATKS

        assert [atk for atk in all_attacks] == EXP_ATKS

    def test_get_cog_attacks_all_levels_fail(self, cogf):
        with pytest.raises(InvalidCogKey):
            get_cog_attacks_all_levels(cog_key=cogf.key + INVALID_COG_KEY)

    @pytest.mark.parametrize(['rel_lvl', 'exp_lvl'],
                             [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
    def test_get_cog_vitals(self, cogf, rel_lvl, exp_lvl):
        vitals = get_cog_vitals(cog_key=cogf.key, relative_level=rel_lvl)
        assert vitals['hp'] == COG_ATTRIBUTES[cogf.key]['hp'][rel_lvl]
        assert vitals['def'] == COG_ATTRIBUTES[cogf.key]['def'][rel_lvl]
        assert vitals['level'] == exp_lvl
        exp_atk_dict = []
        for id, attack_tuple in enumerate(EXP_ATKS):
            exp_atk = {
                'acc': attack_tuple[ATK_IDX_ACC][rel_lvl],
                'cog_key': cogf.key,
                'damage': attack_tuple[ATK_IDX_DMG][rel_lvl],
                'freq': attack_tuple[ATK_IDX_FREQ][rel_lvl],
                'id': id,
                'name': attack_tuple[ATK_IDX_NAME],
                'target': attack_tuple[ATK_IDX_TGT]
            }
            exp_atk_dict.append(exp_atk)
        assert vitals['attacks'] == exp_atk_dict

    def test_get_cog_vitals_fail_key(self, cogf):
        with pytest.raises(InvalidCogKey):
            get_cog_vitals(cog_key=INVALID_COG_KEY)

    @pytest.mark.parametrize('invalid_rel_lvl', INVALID_REL_LVLS[1:])
    def test_get_cog_vitals_fail_level(self, cogf, invalid_rel_lvl):
        with pytest.raises(InvalidRelativeLevel):
            get_cog_vitals(cog_key=cogf.key, relative_level=invalid_rel_lvl)
