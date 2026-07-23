from cmu_graphics import *
import random

class Skill:
    #初始化技能
    def __init__(self,name,button,effect,diceCount,diceSides,fixedDamage,hitBonus,isRanged,range):
        self.name=name
        self.button=button
        self.effect=effect
        self.hitBonus=hitBonus
        self.diceCount=diceCount
        self.diceSides=diceSides
        self.fixedDamage=fixedDamage
        self.isRanged=isRanged
        self.range=range

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

    
