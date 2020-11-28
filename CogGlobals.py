# %%
# Originals:
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/TTLocalizerEnglish.py  # noqa
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/ToontownBattleGlobals.py  # noqa
# TODO: Create docstrings for all functions

from random import randint

debugAttackSequence = {}
COG_ATTRIBUTES = {
    'f': {
        'name': 'Flunky',
        'singularname': 'a Flunky',
        'pluralname': 'Flunkies',
        # 'name': TTLocalizer.SuitFlunky
        # 'singularname': TTLocalizer.SuitFlunkyS,
        # 'pluralname': TTLocalizer.SuitFlunkyP,
        'level': 0,
        'hp': (6, 12, 20, 30, 42),
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


def getActualFromRelativeLevel(name, relLevel):
    data = COG_ATTRIBUTES[name]
    actualLevel = data['level'] + relLevel
    return actualLevel


def get_cog_vitals(name, level=-1):
    data = COG_ATTRIBUTES[name]
    if level == -1:
        level = pickFromFreqList(data['freq'])
    dict = {}
    dict['level'] = getActualFromRelativeLevel(name, level)
    if dict['level'] == 11:
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


def pick_cog_attack(attacks, suitLevel):
    attackNum = None
    randNum = randint(0, 99)
    count = 0
    index = 0
    total = 0
    for c in attacks:
        total = total + c[3][suitLevel]

    for c in attacks:
        count = count + c[3][suitLevel]
        if randNum < count:
            attackNum = index
            break
        index = index + 1

    # configAttackName = config.GetString('attack-type', 'random')
    configAttackName = 'random'  # ! What is this? Where is that config?
    if configAttackName == 'random':
        return attackNum
    elif configAttackName == 'sequence':
        for i in range(len(attacks)):
            if attacks[i] not in debugAttackSequence:
                debugAttackSequence[attacks[i]] = 1
                return i

        return attackNum
    else:
        for i in range(len(attacks)):
            if attacks[i][0] == configAttackName:
                return i

        return attackNum
    return


def get_cog_attack(suitName, suitLevel, attackNum=-1):
    attackChoices = COG_ATTRIBUTES[suitName]['attacks']
    if attackNum == -1:
        # notify.debug('get_cog_attack: picking attacking for %s' % suitName)
        attackNum = pick_cog_attack(attackChoices, suitLevel)
    attack = attackChoices[attackNum]
    adict = {}
    adict['suitName'] = suitName
    name = attack[0]
    adict['name'] = name
    adict['id'] = list(COG_ATTACKS.keys()).index(name)
    adict['animName'] = COG_ATTACKS[name][0]
    adict['hp'] = attack[1][suitLevel]
    adict['acc'] = attack[2][suitLevel]
    adict['freq'] = attack[3][suitLevel]
    adict['group'] = COG_ATTACKS[name][1]
    return adict

# %%
