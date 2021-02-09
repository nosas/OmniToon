# %%
# Originals:
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/TTLocalizerEnglish.py  # noqa
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/ToontownBattleGlobals.py  # noqa
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/battle/SuitBattleGlobals.py  # noqa
# TODO: Create docstrings for all functions

from random import randint

debugAttackSequence = {}
COG_HP = (6, 12, 20, 30, 42, 56, 72, 90, 110, 132, 156, 200)
COG_ATTRIBUTES = {
    'f': {
        'name': 'Flunky',
        'singularname': 'a Flunky',
        'pluralname': 'Flunkies',
        # 'name': TTLocalizer.SuitFlunky
        # 'singularname': TTLocalizer.SuitFlunkyS,
        # 'pluralname': TTLocalizer.SuitFlunkyP,
        'level': 0,  # minimum Cog level
        'hp': COG_HP[0:5],  # Cog levels range from 'level' to 'level'+5
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


def getActualFromRelativeLevel(cog_key, relative_level):
    data = COG_ATTRIBUTES[cog_key]
    actualLevel = data['level'] + relative_level + 1
    return actualLevel


def get_cog_vitals(cog_key, level=-1):
    data = COG_ATTRIBUTES[cog_key]
    if level == -1:
        level = pickFromFreqList(data['freq'])
    dict = {}
    dict['level'] = getActualFromRelativeLevel(cog_key, level)
    if dict['level'] == 11:  # ? why??
        level = 0
    dict['hp'] = data['hp'][level]
    dict['def'] = data['def'][level]
    attacks = data['attacks']
    alist = []
    for a in attacks:
        adict = {}
        name = a[0]
        adict['name'] = name
        adict['animName'] = COG_ATTACKS[name][0]
        adict['hp'] = a[1][level]
        adict['acc'] = a[2][level]
        adict['freq'] = a[3][level]
        adict['group'] = COG_ATTACKS[name][1]
        alist.append(adict)

    dict['attacks'] = alist
    return dict


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

# %%
