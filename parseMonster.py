import sys

def parseDice(section, ):
    infoIndex = section.find('(')
    section = section[infoIndex:]
    critIndex = section.find(';')
    section = section.replace('(', '|')
    section = section.replace('d', '|')
    section = section.replace('+', '|')
    section = section.replace(')', '|')
    section = section.replace(';', '|')
    parts = section.split('|')

    return (int(parts[1]), int(parts[2]), int(parts[3].split()[0]))

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


intList = []
intList.append(('XP', 'xp', 1))
intList.append(('Init', 'init', 1))
intList.append(('Perception', 'perception', 1))
intList.append(('HP', 'maxHitPoints', 2))
intList.append(('EAC ', 'mEAC', 1))
intList.append(('KAC', 'mKAC', 1))
intList.append(('Fort', 'mFort', 1))
intList.append(('Ref', 'mRef', 1))
intList.append(('Will', 'mWill', 1))
intList.append(('Str ', 'strMod', 1))
intList.append(('Dex ', 'dexMod', 1))
intList.append(('Con ', 'conMod', 1))
intList.append(('Int ', 'intMod', 1))
intList.append(('Wis ', 'wisMod', 1))
intList.append(('Cha ', 'chaMod', 1))


lineNum = 0
last = ''
info = {}
for line in lines:
    sections = line.split(';')
    for section in sections:
        parts = section.split()
        if lineNum == 0:
            info['name'] = section[:section.index('(')-1]
        # Parse basic int based stuff
        for element in intList:
            if element[0] in section:
                #print element[0] + " : " + section
                info[element[1]] = int(parts[element[2]])
        # Parse Melee / Ranged
        if "Melee" in section:
            last = 'melee'
            info['mMeleeDice'] = parseDice(section)
        if "Ranged" in section:
            last = 'ranged'
            info['mRangedDice'] = parseDice(section)
        if "critical" in section:
            critInfo = section[1:-1]
            if 'melee' in last:
                info['mMeleeDice'] += (critInfo, )
            if 'ranged' in last:
                info['mRangedDice'] += (critInfo, )
        

    lineNum += 1

dice = ['mMeleeDice', 'mRangedDice']
for dType in dice:
    if dType in info.keys():
        while len(info[dType]) < 4:
            info[dType] += ('', )

objName = info['name'].lower().split()[0] 
sys.stdout.write(objName + " = ")
print info
    
    
    
    
    
    
    
    

    
