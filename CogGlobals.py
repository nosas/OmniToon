# %%
# Originals:
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/TTLocalizerEnglish.py  # noqa
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/ToontownBattleGlobals.py  # noqa
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/battle/SuitBattleGlobals.py  # noqa

from random import randint

debugAttackSequence = {}
ATK_IDX_NAME,  ATK_IDX_TGT, ATK_IDX_DMG, \
    ATK_IDX_ACC, ATK_IDX_FREQ = (0, 1, 2,
                                 3, 4)
ATK_TGT_UNKNOWN, ATK_TGT_SINGLE, ATK_TGT_GROUP = (0, 1, 2)  # previously 1,2,3
COG_HP = (6, 12, 20, 30, 42, 56, 72, 90, 110, 132, 156, 200)
# ! Correct the strange formatting from SuitBattleGlobals with following regex
# \((\d{1,3},)\n\s+(\d{1,3},)\n\s+(\d{1,3},)\n\s+(\d{1,3},)\n\s+(\d{1,3})\)
# ($1 $2 $3 $4 $5)
COG_ATTRIBUTES = {
    'f': {
        'name': 'Flunky',
        'singularname': 'a Flunky',
        'pluralname': 'Flunkies',
        # 'name': TTLocalizer.SuitFlunky
        # 'singularname': TTLocalizer.SuitFlunkyS,
        # 'pluralname': TTLocalizer.SuitFlunkyP,
        # ! TODO: Add 1 to all Cog's minimum levels (Done for BossBots)
        # ! TODO: Add ATK_TGT_ to every cog's attack
        'level': 1,  # minimum Cog level, max level = min_level+4
        'hp': COG_HP[0:5],  # Cog HP range from 'level' to 'level'+5
        'def': (2, 5, 10, 12, 15),
        'freq': (50, 30, 10, 5, 5),
        'acc': (35, 40, 45, 50, 55),
        'attacks': (
            ('PoundKey', ATK_TGT_SINGLE,
                (2, 2, 3, 4, 6),
                (75, 75, 80, 80, 90),
                (30, 35, 40, 45, 50)),
            ('Shred', ATK_TGT_SINGLE,
                (3, 4, 5, 6, 7),
                (50, 55, 60, 65, 70),
                (10, 15, 20, 25, 30)),
            ('ClipOnTie', ATK_TGT_SINGLE,
                (1, 1, 2, 2, 3),
                (75, 80, 85, 90, 95),
                (60, 50, 40, 30, 20))
        )
    },
    'p': {
        'name': 'PencilPusher',
        'level': 2,
        'hp': COG_HP[1:6],
        'def': (5, 10, 15, 20, 25),
        'freq': (50, 30, 10, 5, 5),
        'acc': (45, 50, 55, 60, 65),
        'attacks': (
            ('FountainPen',
                (2, 3, 4, 6, 9),
                (75, 75, 75, 75, 75),
                (20, 20, 20, 20, 20)),
            ('RubOut',
                (4, 5, 6, 8, 12),
                (75, 75, 75, 75, 75),
                (20, 20, 20, 20, 20)),
            ('FingerWag',
                (1, 2, 2, 3, 4),
                (75, 75, 75, 75, 75),
                (35, 30, 25, 20, 15)),
            ('WriteOff',
                (4, 6, 8, 10, 12),
                (75, 75, 75, 75, 75),
                (5, 10, 15, 20, 25)),
            ('FillWithLead',
                (3, 4, 5, 6, 7),
                (75, 75, 75, 75, 75),
                (20, 20, 20, 20, 20))
        )
    },
    'ym': {
        'name': 'Yesman',
        'level': 3,
        'hp': COG_HP[2:7],
        'def': (10, 15, 20, 25, 30),
        'freq': (50, 30, 10, 5, 5),
        'acc': (65, 70, 75, 80, 85),
        'attacks': (
            ('RubberStamp',
                (2, 2, 3, 3, 4),
                (75, 75, 75, 75, 75),
                (35, 35, 35, 35, 35)),
            ('RazzleDazzle',
                (1, 1, 1, 1, 1),
                (50, 50, 50, 50, 50),
                (25, 20, 15, 10, 5)),
            ('Synergy',
                (4, 5, 6, 7, 8),
                (50, 60, 70, 80, 90),
                (5, 10, 15, 20, 25)),
            ('TeeOff',
                (3, 3, 4, 4, 5),
                (50, 60, 70, 80, 90),
                (35, 35, 35, 35, 35))
        )
    },
    'mm': {
        'name': 'Micromanager',
        'level': 4,
        'hp': COG_HP[3:8],
        'def': (15, 20, 25, 30, 35),
        'freq': (50, 30, 10, 5, 5),
        'acc': (70, 75, 80, 82, 85),
        'attacks': (
            ('Demotion',
                (6, 8, 12, 15, 18),
                (50, 60, 70, 80, 90),
                (30, 30, 30, 30, 30)),
            ('FingerWag',
                (4, 6, 9, 12, 15),
                (50, 60, 70, 80, 90),
                (10, 10, 10, 10, 10)),
            ('FountainPen',
                (3, 4, 6, 8, 10),
                (50, 60, 70, 80, 90),
                (15, 15, 15, 15, 15)),
            ('BrainStorm',
                (4, 6, 9, 12, 15),
                (5, 5, 5, 5, 5),
                (25, 25, 25, 25, 25)),
            ('BuzzWord',
                (4, 6, 9, 12, 15),
                (50, 60, 70, 80, 90),
                (20, 20, 20, 20, 20))
        )
    },
    'ds': {
        'name': 'Downsizer',
        'level': 5,
        'hp': COG_HP[4:9],
        'def': (20, 25, 30, 35, 40),
        'freq': (50, 30, 10, 5, 5),
        'acc': (35, 40, 45, 50, 55),
        'attacks': (
            ('Canned',
                (5, 6, 8, 10, 12),
                (60, 75, 80, 85, 90),
                (25, 25, 25, 25, 25)),
            ('Downsize',
                (8, 9, 11, 13, 15),
                (50, 65, 70, 75, 80),
                (35, 35, 35, 35, 35)),
            ('PinkSlip',
                (4, 5, 6, 7, 8),
                (60, 65, 75, 80, 85),
                (25, 25, 25, 25, 25)),
            ('Sacked',
                (5, 6, 7, 8, 9),
                (50, 50, 50, 50, 50),
                (15, 15, 15, 15, 15))
        )
    },
    'hh': {
        'name': 'HeadHunter',
        'level': 6,
        'hp': COG_HP[5:10],
        'def': (25, 30, 35, 40, 45),
        'freq': (50, 30, 10, 5, 5),
        'acc': (35, 40, 45, 50, 55),
        'attacks': (
            ('FountainPen',
                (5, 6, 8, 10, 12),
                (60, 75, 80, 85, 90),
                (15, 15, 15, 15, 15)),
            ('GlowerPower',
                (7, 8, 10, 12, 13),
                (50, 60, 70, 80, 90),
                (20, 20, 20, 20, 20)),
            ('HalfWindsor',
                (8, 10, 12, 14, 16),
                (60, 65, 70, 75, 80),
                (20, 20, 20, 20, 20)),
            ('HeadShrink',
                (10, 12, 15, 18, 21),
                (65, 75, 80, 85, 95),
                (35, 35, 35, 35, 35)),
            ('Rolodex',
                (6, 7, 8, 9, 10),
                (60, 65, 70, 75, 80),
                (10, 10, 10, 10, 10))
        )
    },
    'cr': {
        'name': 'CorporateRaider',
        'level': 7,
        'hp': COG_HP[6:11],
        'def': (30, 35, 40, 45, 50),
        'freq': (50, 30, 10, 5, 5),
        'acc': (35, 40, 45, 50, 55),
        'attacks': (
            ('Canned',
                (6, 7, 8, 9, 10),
                (60, 75, 80, 85, 90),
                (20, 20, 20, 20, 20)),
            ('EvilEye',
                (12, 15, 18, 21, 24),
                (60, 70, 75, 80, 90),
                (35, 35, 35, 35, 35)),
            ('PlayHardball',
                (7, 8, 12, 15, 16),
                (60, 65, 70, 75, 80),
                (30, 30, 30, 30, 30)),
            ('PowerTie',
                (10, 12, 14, 16, 18),
                (65, 75, 80, 85, 95),
                (15, 15, 15, 15, 15))
        )
    },
    'tbc': {
        'name': 'TheBigCheese',
        'level': 8,
        'hp': COG_HP[7:12],
        'def': (35, 40, 45, 50, 55),
        'freq': (50, 30, 10, 5, 5),
        'acc': (35, 40, 45, 50, 55),
        'attacks': (
            ('CigarSmoke',
                (10, 12, 15, 18, 20),
                (55, 65, 75, 85, 95),
                (20, 20, 20, 20, 20)),
            ('FloodTheMarket',
                (14, 16, 18, 20, 22),
                (70, 75, 85, 90, 95),
                (10, 10, 10, 10, 10)),
            ('SongAndDance',
                (14, 15, 17, 19, 20),
                (60, 65, 70, 75, 80),
                (20, 20, 20, 20, 20)),
            ('TeeOff',
                (8, 11, 14, 17, 20),
                (55, 65, 70, 75, 80),
                (50, 50, 50, 50, 50))
        )
    }
}

# ! Create get_cog_atk_tgt(atk_name=cog_attack['name']), return 0,1,2
COG_ATTACKS = {
    'PoundKey': ('phone', ATK_TGT_SINGLE),
    'Shred': ('shredder', ATK_TGT_SINGLE),
    'ClipOnTie': ('throw-paper', ATK_TGT_SINGLE)
}
# Cog attack indexes
CLIPON_TIE = list(COG_ATTACKS.keys()).index('ClipOnTie')
POUND_KEY = list(COG_ATTACKS.keys()).index('PoundKey')
SHRED = list(COG_ATTACKS.keys()).index('Shred')


# TODO Add docstring, picks cog level based on cog's freq values
def pickFromFreqList(freqList):
    rand_num = randint(0, 99)
    count = 0
    index = 0
    level = None
    for f in freqList:
        count = count + f
        if rand_num < count:
            level = index
            break
        index = index + 1

    return level


# TODO Add docstring and rename to snake case
def get_actual_from_relative_level(cog_key, relative_level):
    cog_data = COG_ATTRIBUTES[cog_key]
    assert relative_level in range(5), (
            "ERROR: Variable `relative_level` must be in the values "
            "[0, 1, 2, 3, 4], where 0 is the mininmum Cog level and 4 is the "
            "maximum Cog level."
    )
    actual_level = cog_data['level'] + relative_level
    return actual_level


def get_cog_vitals(cog_key, relative_level=-1):
    """Return dictionary of Cog's vitals

    Args:
        cog_key (str): [description]
        relative_level (int, optional): Relative level from 0-4. Defaults to -1

    Returns:
        vitals_dict:

    Example:
        {
            'name': 'Flunky',
            'level': 5,
            'hp': 42,
            'def': 15,
            'attacks': [
                {
                    'acc': 80,
                    'animName': 'phone',
                    'freq': 40,
                    'hp': 3,
                    'id': 0,
                    'name': 'PoundKey',
                    'target': 1  # ATK_TGT_SINGLE=1, ATK_TGT_GROUP=2
                }
                {
                    'acc': 70,
                    'animName': 'shredder',
                    'freq': 30,
                    'hp': 7,
                    'id': 1,
                    'name': 'Shred',
                    'target': 1
                },
                {
                    'acc': 95,
                    'animName': 'throw-paper',
                    'freq': 20,
                    'hp': 3,
                    'id': 2,
                    'name': 'ClipOnTie',
                    'target': 1
                }
            ]
        }
    """
    cog_data = COG_ATTRIBUTES[cog_key]
    # Pick random Cog level
    if relative_level == -1:
        relative_level = pickFromFreqList(cog_data['freq'])
    vitals_dict = {}
    vitals_dict['level'] = get_actual_from_relative_level(cog_key, relative_level)
    if vitals_dict['level'] == 11:  # ? why??
        relative_level = 0
    vitals_dict['hp'] = cog_data['hp'][relative_level]
    vitals_dict['def'] = cog_data['def'][relative_level]

    attacks = cog_data['attacks']
    all_attacks_list = []
    cur_index = 0
    for attack in attacks:
        attacks_dict = {}
        attack_name = attack[0]
        attacks_dict['acc'] = attack[ATK_IDX_ACC][relative_level]
        attacks_dict['animName'] = COG_ATTACKS[attack_name][0]
        attacks_dict['freq'] = attack[ATK_IDX_FREQ][relative_level]
        attacks_dict['hp'] = attack[ATK_IDX_DMG][relative_level]
        attacks_dict['id'] = cur_index
        attacks_dict['name'] = attack_name
        attacks_dict['target'] = attack[ATK_IDX_TGT]  # Peviously group
        # attacks_dict['group'] = COG_ATTACKS[attack_name][1]
        all_attacks_list.append(attacks_dict)
        cur_index += 1

    vitals_dict['attacks'] = all_attacks_list
    return vitals_dict


def pick_cog_attack(attack_choices, relative_level):
    """ Summary: Return the attack_index of cog attack from cog.vitals['attacks']

    """
    attack_index = None
    # import pdb;pdb.set_trace()
    rand_num = randint(0, 99)
    count = 0
    cur_index = 0
    """

    """
    for attack in attack_choices:
        atk_frequency = attack[ATK_IDX_FREQ][relative_level]
        count = count + atk_frequency
        if rand_num < count:
            attack_index = cur_index
            break
        cur_index = cur_index + 1

    # configAttackName = config.GetString('attack-type', 'random')
    configAttackName = 'random'  # ! What is this? Where is that config?
    if configAttackName == 'random':
        return attack_index
    else:
        assert configAttackName == 'random', "How is this not random?"
        # elif configAttackName == 'sequence':
        #     for i in range(len(attack_choices)):
        #         if attack_choices[i] not in debugAttackSequence:
        #             debugAttackSequence[attack_choices[i]] = 1
        #             return i

        #     return attack_index
        # else:
        #     for i in range(len(attack_choices)):
        #         if attack_choices[i][0] == configAttackName:
        #             return i

        #     return attack_index
        # return


def get_cog_attacks_all_levels(cog_key):
    """Return tuple containing all possible Cog attack choices for a single Cog

    Args:
        cog_key (str): Cog key, short-hand of the Cog's name

    Returns:
        attack_choices (tuple): All possible Cog attack choices
        example ::
                    'attacks': (
                        ('PoundKey',                [0] Name
                            (2, 2, 3, 4, 6),        [1] Damage
                            (75, 75, 80, 80, 90),   [2] Accuracy
                            (30, 35, 40, 45, 50)),  [3] Frequency
                        ('Shred',
                            (3, 4, 5, 6, 7),
                            (50, 55, 60, 65, 70),
                            (10, 15, 20, 25, 30)),
                        ('ClipOnTie',
                            (1, 1, 2, 2, 3),
                            (75, 80, 85, 90, 95),
                            (60, 50, 40, 30, 20))
                    )
    """
    return COG_ATTRIBUTES[cog_key]['attacks']


# TODO Refactor the variable names in this function
def get_cog_attack(cog_key, relative_level, attack_index=-1):
    """Return dictionary of Cog's attack given COG_ATTR key and relative_level

    Args:
        cog_key (str): Key value for COG_ATTRIBUTES of the Cog's name.
                        e.g. 'f' for Flunky, 'p' for PencilPusher
        relative_level (int): Relative level of the Cog (0-4)
        attack_index (int, optional): Defaults to -1, selects random attack.

    Returns:
        dict: Dictionary containing cog key, atk name/id/hp(dmg)/acc/freq etc.

        Attack dictionary example of lvl 2 Flunky ::
            {
                'cog_key': 'f',
                'name': 'PoundKey',
                'id': 0,
                'animName': 'phone',
                'hp': 3,
                'acc': 80,
                'freq': 40,
                'target': 2  # ATK_TGT_SINGLE=1, ATK_TGT_GROUP=2
            }
    """
    # attackChoices = COG_ATTRIBUTES[cog_key]['attacks']
    attackChoices = get_cog_attacks_all_levels(cog_key=cog_key)
    if attack_index == -1:
        # notify.debug('get_cog_attack: picking attacking for %s' % cog_key)
        attack_index = pick_cog_attack(attackChoices, relative_level)
    attack_tuple = attackChoices[attack_index]
    """ Example attack tuple ::
                (
                    'PoundKey', ATK_TGT_SINGLE, # Name, Target
                    (2, 2, 3, 4, 6),            # Dmg
                    (75, 75, 80, 80, 90),       # Acc
                    (30, 35, 40, 45, 50)        # Freq
                )
    """
    attack_dict = {}
    attack_dict['cog_key'] = cog_key
    attack_name = attack_tuple[ATK_IDX_NAME]
    attack_dict['name'] = attack_name
    attack_dict['id'] = list(COG_ATTACKS.keys()).index(attack_name)
    attack_dict['animName'] = COG_ATTACKS[attack_name][0]
    attack_dict['hp'] = attack_tuple[ATK_IDX_DMG][relative_level]
    attack_dict['acc'] = attack_tuple[ATK_IDX_ACC][relative_level]
    attack_dict['freq'] = attack_tuple[ATK_IDX_FREQ][relative_level]
    attack_dict['target'] = attack_tuple[ATK_IDX_TGT]  # previously group
    # attack_dict['group'] = COG_ATTACKS[attack_name][1]
    return attack_dict
