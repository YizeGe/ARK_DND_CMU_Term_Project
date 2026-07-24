from cmu_graphics import *
import random

class Skill:
    #初始化技能
    def __init__(self,name,button,effect,diceCount,diceSides,fixedDamage,hitBonus,isRanged,range,costAction,costBonus,costReaction,costRingSlot):
        self.name=name
        self.button=button
        self.effect=effect
        self.hitBonus=hitBonus
        self.diceCount=diceCount
        self.diceSides=diceSides
        self.fixedDamage=fixedDamage
        self.isRanged=isRanged
        self.range=range
        self.costAction=costAction
        self.costBonus=costBonus
        self.costReaction=costReaction
        self.costRingSlot=costRingSlot

    def isHit(self,ac):
        roll=self.rollDice()+self.hitBonus
        if roll>=ac:
            return True
        else:
            return False

    def calDamage(self,attacker):
        sumDamage=0
        for _ in range(self.diceCount):
            sumDamage+=self.rollDamage()
        sumDamage+=self.fixedDamage
        if self.isRanged:
            sumDamage+=attacker.calculateBonus(attacker.dexterity)
        else:
            sumDamage+=attacker.calculateBonus(attacker.strength)
        return sumDamage

    def rollDamage(self):
        return random.randint(1,self.diceSides)

    def rollDice(self):
        return random.randint(1,20)

    def canUse(self,unit):
        if self.costAction and unit.act<1:
            return False
        if self.costBonus and unit.bonus_used:
            return False
        if self.costReaction and unit.reaction_used:
            return False
        if self.costRingSlot==1 and unit.ring1<1:
            return False
        if self.costRingSlot==2 and unit.ring2<1:
            return False
        return True

    def consumeResources(self,unit):
        if self.canUse(unit):
            if self.costAction:
                unit.act-=1
            if self.costBonus:
                unit.bonus_used=True
            if self.costReaction:
                unit.reaction_used=True
            if self.costRingSlot==1:
                unit.ring1-=1
            if self.costRingSlot==2:
                unit.ring2-=1
            return True
        return False
