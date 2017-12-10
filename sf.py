import code
from copy import  deepcopy
from random import *

from monsters import *

modifier = [-5,-5,-4,-4,-3,-3,-2,-2,-1,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8]
expLevels = [0, 0, 1300, 3300, 6000, 10000, 15000, 23000, 34000, 50000, 
            71000, 105000, 145000, 210000, 295000, 425000, 600000, 
            850000,1200000,1700000,2400000]

def statByMod(stat):
    index = 0
    for value in modifier:
        if value == stat:
            return index
        index += 1
    return 0

class mob:
    def __init__(self, name, monsterDict = None):
        self.name = name

        self.str = 0
        self.dex = 0
        self.con = 0
        self.int = 0
        self.wis = 0
        self.cha = 0

        self.damageResist = 0
        self.baseAttk = 0
        self.fortSave = 0
        self.reflSave = 0
        self.willSave = 0

        self.level = 0
        self.exp = 0

        self.maxStamina = 0
        self.maxHitPoints = 0
        self.maxResolvePoints = 0

        self.curStamina = 0
        self.curHitPoints = 0
        self.curResolvePoints = 0
        self.curInit = 0
        self.init = 0
        self.perception = 0

        self.earmor = 0
        self.karmor = 0
        self.skills = {}

        # for monsters
        self.monster = False
        self.mEAC = 0
        self.mKAC = 0
        self.mFort = 0
        self.mRef = 0
        self.mWill = 0
        self.mMeleeDice = (0,0,0, '')
        self.mRangedDice = (0,0,0, '')
        self.mThrowDice = (0,0,0, '')

        if monsterDict != None:
            self.initFromDict(monsterDict)

    def initFromDict(self, monsterDict):
        self.monster = True
        for key in monsterDict.keys():
            if 'Mod' in key:
                setattr(self, key, statByMod(monsterDict[key]))
            else:
                setattr(self, key, monsterDict[key])

    def getEac(self, mod=0):
        if self.mEAC != 0:
            return self.mEAC
        return 10 + self.earmor + modifier[self.dex] + mod

    def getKac(self, mod=0):
        if self.mKAC != 0:
            return self.mKAC
        return 10 + self.karmor + modifier[self.dex] + mod

    def getACvsCM(self):
        return 8 + getKac(0)

    def getInit(self, mod=0):
        return modifier[self.dex] + mod + self.init

    def getFort(self, mod):
        if self.mFort != 0:
            return self.mFort
        return self.fortSave + modifier[self.con] + mod

    def getReflex(self, mod=0):
        if self.mRef != 0:
            return self.mRef
        return self.reflSave + modifier[self.dex] + mod

    def getWill(self, mod=0):
        if self.mWill != 0:
            return self.mWill
        return self.willSave + modifier[self.wis] + mod

    def getMelee(self, mod=0):
        return self.baseAttk + modifier[self.str] + mod
    
    def getRanged(self, mod=0):
        return self.baseAttk + modifier[self.dex] + mod
    
    def getThrown(self, mod=0):
        return getMele(mod)

    def addExp(self, exp):
        self.exp += exp
        if self.exp >= expLevels[self.level+1]:
            self.level += 1
        return self.exp

class encounter:
    def __init__(self, combatants, perceptionCheck = 0):
        self.combatants = combatants
        self.order = []

        if perceptionCheck > 0:
            self.checkPerception(perceptionCheck)

        self.getOrder()

    def checkPerception(self, check):
        for combatant in self.combatants:
            roll = randint(1,20) + combatant.perception
            if roll > check:
                print combatant.name + " PASSED perception with " + str(roll)
            else:
                print combatant.name + " FAILED perception with " + str(roll)


    def getOrder(self):
        order = {}
        for mob in self.combatants:
            mob.curInit = mob.getInit() + randint(1,20)
            order[mob.curInit] = mob

        for key in reversed(sorted(order.iterkeys())):
            self.order.append(order[key])
            print str(key) + ": " +  order[key].name
       
    def showOrder(self):
        for combatant in self.order:
            print str(combatant.curInit) + ": " + combatant.name


def attk(mob1, mob2, typeAttk, mod1=0, mod2=0):
    energy = 0
    kinetic = 0
    grab = 0
    melee = 0
    ranged = 0
    throw = 0

    mob1Attk = 0
    mob2Def = 0

    if 'e' in typeAttk:
        energy = 1
        mob2Def = mob2.getEac()
    if 'k' in typeAttk:
        kinetic = 1
        mob2Def = mob2.getKac()
    if 'g' in typeAttk:
        grab = 1
        melee = 1
        mob2Def = mob2.getACvsCM()
    if 'm' in typeAttk:
        melee = 1
        mob1Attk = mob1.getMelee()
    if 'r' in typeAttk:
        ranged = 1
        mob1Attk = mob1.getRanged()
    if 't' in typeAttk:
        throw = 1
        mob1Attk = mob1.getThrown()

    roll = mob2Def - mob1Attk
    print mob1.name + " hits " + mob2.name + " if roll >= " + str(roll)

    if mob1.monster == True:
        toHit = randint(1,20)
        print mob1.name + " rolls " + str(toHit)
        if toHit >= roll:
            if melee == 1:
                dice = mob1.mMeleeDice
            if ranged == 1:
                dice = mob1.mRangedDice
            if throw == 1:
                dice = mob1.mThrownDice

            numDice = dice[0]
            dWhat = dice[1]
            baseMod = dice[2]
            critText = dice[3]

            if toHit == 20:
                print "CRIT! " + critText
                
            damage = 0
            for i in range(0, numDice):
                damage += randint(1,dWhat)
            damage += baseMod
            damage -= mob2.damageResist

            print mob1.name + " hits " + mob2.name + " for " + str(damage) + " damage"
            dmg(mob2, damage)

def dmg(mob, damage):
    mob.curHitPoints -= (damage - mob.damageResist)
    if mob.curHitPoints < 1:
        print mob.name + " HAS DIED."
    else:
        print mob.name + " has " + str(mob.curHitPoints) + " HP left"

def heal(mob, health):
    mob.curHitPoints += health
    if mob.curHitPoints > mob.maxHitPoints:
        mob.curHitPoints = mob.maxHitPoints
        print mob.name + " is maxed out at " + str(mob.curHitPoints) + " HP"
    else:
        print mob.name + " has " + str(mob.curHitPoints) + " HP"

def roll(dWhat):
    rolled = randint(1,dWhat)
    print "Rolled a d" + str(dWhat) + ": " + str(rolled)
    return rolled


# CHARACTERS
fiblu = mob('Fiblu')
fiblu.str = 11
fiblu.dex = 12
fiblu.com = 10
fiblu.int = 8
fiblu.wis = 10
fiblu.cha = 12
fiblu.maxHitPoints = 9
fiblu.curHitPoints = 9
fiblu.maxStamina = 7
fiblu.curStamina = 7
fiblu.baseAttack = 1
fiblu.fortSave = 2
fiblu.willSave = 2
fiblu.skills['acrobatics'] = 5
fiblu.skills['athletics'] = 5
fiblu.skills['intimidate'] = 5

ace = mob('Ace')
ace.str = 11
ace.dex = 12
ace.com = 12
ace.int = 14
ace.wis = 9
ace.cha = 15
ace.maxHitPoints = 10
ace.curHitPoints = 10
ace.maxStamina = 7
ace.curStamina = 7
ace.baseAttack = 0
ace.reflSave = 2
ace.willSave = 2
ace.skills['acrobatics'] = 5
ace.skills['athletics'] = 5
ace.skills['computers'] = 6
ace.skills['culture'] = 6
ace.skills['diplomacy'] = 6
ace.skills['intimidate'] = 6
ace.skills['orator'] = 6
ace.skills['sense motive'] = 1
ace.skills['sleight of hand'] = 5

traks = mob('Traks')
traks.str = 12
traks.dex = 14
traks.com = 13                   
traks.int = 16
traks.wis = 10
traks.cha = 8
traks.maxHitPoints = 11
traks.curHitPoints = 11
traks.maxStamina = 6
traks.curStamina = 6
traks.earmor = 1
traks.karmor = 1
traks.baseAttack = 0
traks.willSave = 2

josh = mob('Josh')
josh.str = 11
josh.dex = 16
josh.com = 10
josh.int = 17
josh.wis = 11
josh.cha = 18
josh.maxHitPoints = 10
josh.curHitPoints = 10
josh.maxStamina = 6
josh.curStamina = 6
josh.baseAttack = 0
josh.fortSave = 2
josh.reflSave = 2
josh.skills['computers'] = 8
josh.skills['athletics'] = 4
josh.skills['engineering'] = 8
josh.skills['medicine'] = 7
josh.skills['perception'] = 4
josh.skills['piloting'] = 8
josh.skills['electrician'] = 7

erin = mob('Erin')
erin.str = 13
erin.dex = 10
erin.com = 12
erin.int = 11
erin.wis = 9
erin.cha = 18
erin.maxHitPoints = 13
erin.curHitPoints = 13
erin.maxStamina = 8
erin.curStamina = 8
erin.baseAttack = 1
erin.fortSave = 2
erin.willSave = 2
erin.skills['acrobatics'] = 4
erin.skills['medicine'] = 1
erin.skills['mysticism'] = 3
erin.skills['physical science'] = 4


nalani = mob('Nalani')
nalani.str = 10
nalani.dex = 10
nalani.com = 13
nalani.int = 12
nalani.wis = 16
nalani.cha = 12
nalani.maxHitPoints = 10
nalani.curHitPoints = 10
nalani.maxStamina = 7
nalani.curStamina = 7
nalani.baseAttack = 0
nalani.willSave = 2


# MONSTER BASE TYPES

absalomMob = mob(absalom['name'], absalom)
jabaxaMob = mob(jabaxa['name'], jabaxa)
downsideMob = mob(downside['name'], downside)

code.interact(local=locals())
