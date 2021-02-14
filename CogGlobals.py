# %%
# Originals:
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/TTLocalizerEnglish.py  # noqa
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/ToontownBattleGlobals.py  # noqa
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/battle/SuitBattleGlobals.py  # noqa

from random import randint

debugAttackSequence = {}
COG_HP = (6, 12, 20, 30, 42, 56, 72, 90, 110, 132, 156, 200)
# ! Correct the strange formatting from SuitBattleGlobalS with following regex
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
        # ! TODO: Add 1 to all Cog's minimum levels
        'level': 1,  # minimum Cog level, max level = min_level+4
        'hp': COG_HP[0:5],  # Cog HP range from 'level' to 'level'+5
        'def': (2, 5, 10, 12, 15),
        'freq': (50, 30, 10, 5, 5),
        'acc': (35, 40, 45, 50, 55),
        'attacks': (
            ('PoundKey',
                (2, 2, 3, 4, 6),
                (75, 75, 80, 80, 90),
                (30, 35, 40, 45, 50)),
            ('Shred',
                (3, 4, 5, 6, 7),
                (50, 55, 60, 65, 70),
                (10, 15, 20, 25, 30)),
            ('ClipOnTie',
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


ATK_TGT_UNKNOWN = 1
ATK_TGT_SINGLE = 2
ATK_TGT_GROUP = 3
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
    randNum = randint(0, 99)
    count = 0
    index = 0
    level = None
    for f in freqList:
        count = count + f
        if randNum < count:
            level = index
            break
        index = index + 1

    return level


# TODO Add docstring and rename to snake case
def getActualFromRelativeLevel(cog_key, relative_level):
    cog_data = COG_ATTRIBUTES[cog_key]
    actualLevel = cog_data['level'] + relative_level
    return actualLevel


def get_cog_vitals(cog_key, relative_level=-1):
    """Return dictionary of Cog's vitals

    Args:
        cog_key (str): [description]
        relative_level (int, optional): Relative level from 0-4. Defaults to -1

    Returns:
        vitals_dict:

    Example:
        {
            'level': 5,
            'hp': 42,
            'def': 15,
            'attacks': [
                {
                    'name': 'PoundKey',
                    'animName': 'phone',
                    'hp': 6, 'acc': 90,
                    'freq': 50,
                    'group': 2
                },
                {
                    'name': 'Shred',
                    'animName': 'shredder',
                    'hp': 7,
                    'acc': 70,
                    'freq': 30,
                    'group': 2
                },
                {
                    'name': 'ClipOnTie',
                    'animName': 'throw-paper',
                    'hp': 3,
                    'acc': 95,
                    'freq': 20,
                    'group': 2
                }
            ]
        }
    """
    cog_data = COG_ATTRIBUTES[cog_key]
    if relative_level == -1:
        relative_level = pickFromFreqList(cog_data['freq'])
    vitals_dict = {}
    vitals_dict['level'] = getActualFromRelativeLevel(cog_key, relative_level)
    if vitals_dict['level'] == 11:  # ? why??
        relative_level = 0
    vitals_dict['hp'] = cog_data['hp'][relative_level]
    vitals_dict['def'] = cog_data['def'][relative_level]

    attacks = cog_data['attacks']
    attacks_list = []
    for attack in attacks:
        attacks_dict = {}
        attack_name = attack[0]
        attacks_dict['name'] = attack_name
        attacks_dict['animName'] = COG_ATTACKS[attack_name][0]
        attacks_dict['hp'] = attack[1][relative_level]
        attacks_dict['acc'] = attack[2][relative_level]
        attacks_dict['freq'] = attack[3][relative_level]
        attacks_dict['group'] = COG_ATTACKS[attack_name][1]
        attacks_list.append(attacks_dict)

    vitals_dict['attacks'] = attacks_list
    return vitals_dict


def pick_cog_attack(attacks, cog_level):
    attack_num = None
    randNum = randint(0, 99)
    count = 0
    index = 0
    total = 0
    for c in attacks:
        total = total + c[3][cog_level]

    for c in attacks:
        count = count + c[3][cog_level]
        if randNum < count:
            attack_num = index
            break
        index = index + 1

    # configAttackName = config.GetString('attack-type', 'random')
    configAttackName = 'random'  # ! What is this? Where is that config?
    if configAttackName == 'random':
        return attack_num
    elif configAttackName == 'sequence':
        for i in range(len(attacks)):
            if attacks[i] not in debugAttackSequence:
                debugAttackSequence[attacks[i]] = 1
                return i

        return attack_num
    else:
        for i in range(len(attacks)):
            if attacks[i][0] == configAttackName:
                return i

        return attack_num
    return


# TODO Refactor the variable names in this function
def get_cog_attack(cog_key, cog_level, attack_num=-1):
    """Return dictionary of Cog's attack given cog_attr name and cog_level

    Args:
        cog_key (str): Key value for COG_ATTRBIUTES of the Cog's name.
                        e.g. 'f' for Flunky, 'p' for PencilPusher
        cog_level (int): Level of the Cog
        attack_num (int, optional): Defaults to -1, selects random attack.

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
                'group': 2  # ATK_TGT_SINGLE=2, ATK_TGT_GROUP=3
            }
    """
    attackChoices = COG_ATTRIBUTES[cog_key]['attacks']
    if attack_num == -1:
        # notify.debug('get_cog_attack: picking attacking for %s' % cog_key)
        attack_num = pick_cog_attack(attackChoices, cog_level)
    attack = attackChoices[attack_num]
    adict = {}
    adict['cog_key'] = cog_key
    name = attack[0]
    adict['name'] = name
    adict['id'] = list(COG_ATTACKS.keys()).index(name)
    adict['animName'] = COG_ATTACKS[name][0]
    adict['hp'] = attack[1][cog_level]
    adict['acc'] = attack[2][cog_level]
    adict['freq'] = attack[3][cog_level]
    adict['group'] = COG_ATTACKS[name][1]
    return adict
